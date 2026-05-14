import os
from fastapi import APIRouter
from config import DATA_DIR
from services import parser, vector_store

router = APIRouter(tags=["documents"])


@router.get("/documents")
def list_documents():
    stats = vector_store.get_document_stats()
    return {"documents": stats}


@router.post("/documents/index")
def index_documents():
    if not os.path.isdir(DATA_DIR):
        return {"status": "empty", "message": "data/ 目录不存在，请先创建并放入PDF文件"}

    pdf_files = [f for f in os.listdir(DATA_DIR) if f.lower().endswith(".pdf")]
    if not pdf_files:
        return {"status": "empty", "message": "data/ 目录中没有PDF文件，请先放入文档"}

    vector_store.clear_all()
    total_chunks = 0
    files_processed = 0

    for pdf_file in pdf_files:
        filepath = os.path.join(DATA_DIR, pdf_file)
        try:
            chunks = parser.parse_pdf(filepath)
            if chunks:
                vector_store.add_chunks(chunks)
                total_chunks += len(chunks)
                files_processed += 1
        except Exception as e:
            return {"status": "error", "message": f"处理 {pdf_file} 失败: {str(e)}"}

    return {
        "status": "ok",
        "files_processed": files_processed,
        "total_chunks": total_chunks,
        "message": f"成功索引 {files_processed} 个文件，共 {total_chunks} 个分块",
    }
