import uuid
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, require_role
from app.models.user import UserRole, User
from app.schemas.resume import ResumeUploadResponse, ResumeResponse, ResumeListResponse
from app.services.resume_service import ResumeService

router = APIRouter(prefix="/resumes", tags=["Resumes"])


@router.post("/upload", response_model=ResumeUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    current_user: User = Depends(require_role(UserRole.STUDENT)),
    db: AsyncSession = Depends(get_db),
    file: UploadFile = File(..., description="Resume PDF file"),
):
    """
    Upload resume PDF for parsing and analysis (students only).
    
    Process:
    1. Save file to local storage
    2. Parse PDF and extract text
    3. Extract skills using skill ontology
    4. Build structured profile
    5. Calculate resume score
    6. Update student profile automatically
    7. Generate embeddings and store in Qdrant
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported"
        )
    
    # Validate file size (max 10MB)
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size must be less than 10MB"
        )
    
    # Get student profile
    from app.services.student_service import StudentService
    student_service = StudentService()
    student = await student_service.get_student_by_user_id(db, current_user.id)
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )
    
    # Process resume
    service = ResumeService()
    try:
        resume = await service.upload_and_process_resume(
            db=db,
            student_id=student.id,
            file_content=content,
            filename=file.filename
        )
        
        return ResumeUploadResponse(
            id=resume.id,
            status=resume.status,
            original_filename=resume.original_filename,
            message="Resume uploaded and processed successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process resume: {str(e)}"
        )


@router.get("/me", response_model=ResumeListResponse)
async def get_my_resumes(
    current_user: User = Depends(require_role(UserRole.STUDENT)),
    db: AsyncSession = Depends(get_db),
):
    """Get all resumes for current student."""
    from app.services.student_service import StudentService
    student_service = StudentService()
    student = await student_service.get_student_by_user_id(db, current_user.id)
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )
    
    service = ResumeService()
    resumes = await service.get_student_resumes(db, student.id)
    
    return ResumeListResponse(
        resumes=[ResumeResponse.model_validate(r) for r in resumes],
        total=len(resumes)
    )


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: uuid.UUID,
    current_user: User = Depends(require_role(UserRole.STUDENT)),
    db: AsyncSession = Depends(get_db),
):
    """Get resume details by ID (students only, own resumes)."""
    service = ResumeService()
    resume = await service.get_resume_by_id(db, resume_id)
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Verify ownership
    from app.services.student_service import StudentService
    student_service = StudentService()
    student = await student_service.get_student_by_user_id(db, current_user.id)
    
    if not student or resume.student_id != student.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return ResumeResponse.model_validate(resume)
