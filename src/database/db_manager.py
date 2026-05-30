"""
Database Manager - Abstract Layer
Supports JSON (current) and SQLite (future)
"""

from abc import ABC, abstractmethod
from typing import Any, List, Dict, Optional
import json
from pathlib import Path
import uuid
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DatabaseAdapter(ABC):
    """Abstract base class for database adapters"""
    
    @abstractmethod
    def create(self, collection: str, data: Dict[str, Any]) -> str:
        """Create a new record"""
        pass
    
    @abstractmethod
    def read(self, collection: str, record_id: str) -> Optional[Dict[str, Any]]:
        """Read a record by ID"""
        pass
    
    @abstractmethod
    def update(self, collection: str, record_id: str, data: Dict[str, Any]) -> bool:
        """Update a record"""
        pass
    
    @abstractmethod
    def delete(self, collection: str, record_id: str) -> bool:
        """Delete a record"""
        pass
    
    @abstractmethod
    def query(self, collection: str, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Query records with filters"""
        pass
    
    @abstractmethod
    def list_all(self, collection: str) -> List[Dict[str, Any]]:
        """List all records in collection"""
        pass

class JSONAdapter(DatabaseAdapter):
    """JSON file-based database adapter"""
    
    def __init__(self, data_dir: Path):
        """
        Initialize JSON adapter
        
        Args:
            data_dir: Directory to store JSON files
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._ensure_collections()
    
    def _get_collection_path(self, collection: str) -> Path:
        """Get path for collection file"""
        return self.data_dir / f"{collection}.json"
    
    def _ensure_collections(self):
        """Ensure all required collections exist"""
        collections = [
            "users", "licenses", "transactions", "api_changes",
            "bots", "audit_logs"
        ]
        for collection in collections:
            path = self._get_collection_path(collection)
            if not path.exists():
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump({"data": []}, f, indent=2)
    
    def _load_collection(self, collection: str) -> Dict[str, Any]:
        """Load collection from file"""
        path = self._get_collection_path(collection)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.warning(f"Corrupted JSON file: {path}. Initializing with empty data.")
            return {"data": []}
    
    def _save_collection(self, collection: str, data: Dict[str, Any]) -> None:
        """Save collection to file"""
        path = self._get_collection_path(collection)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def create(self, collection: str, data: Dict[str, Any]) -> str:
        """Create a new record with auto-generated ID"""
        record_id = str(uuid.uuid4())
        data["id"] = record_id
        data["created_at"] = datetime.utcnow().isoformat()
        
        collection_data = self._load_collection(collection)
        collection_data["data"].append(data)
        self._save_collection(collection, collection_data)
        
        logger.debug(f"Created record in {collection}: {record_id}")
        return record_id
    
    def read(self, collection: str, record_id: str) -> Optional[Dict[str, Any]]:
        """Read a record by ID"""
        collection_data = self._load_collection(collection)
        
        for record in collection_data.get("data", []):
            if record.get("id") == record_id:
                return record
        
        return None
    
    def update(self, collection: str, record_id: str, data: Dict[str, Any]) -> bool:
        """Update a record"""
        collection_data = self._load_collection(collection)
        
        for i, record in enumerate(collection_data.get("data", [])):
            if record.get("id") == record_id:
                data["updated_at"] = datetime.utcnow().isoformat()
                collection_data["data"][i].update(data)
                self._save_collection(collection, collection_data)
                logger.debug(f"Updated record in {collection}: {record_id}")
                return True
        
        return False
    
    def delete(self, collection: str, record_id: str) -> bool:
        """Delete a record"""
        collection_data = self._load_collection(collection)
        original_len = len(collection_data.get("data", []))
        
        collection_data["data"] = [
            r for r in collection_data.get("data", [])
            if r.get("id") != record_id
        ]
        
        if len(collection_data["data"]) < original_len:
            self._save_collection(collection, collection_data)
            logger.debug(f"Deleted record from {collection}: {record_id}")
            return True
        
        return False
    
    def query(self, collection: str, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Query records with filters"""
        collection_data = self._load_collection(collection)
        results = []
        
        for record in collection_data.get("data", []):
            match = True
            for key, value in filters.items():
                if record.get(key) != value:
                    match = False
                    break
            if match:
                results.append(record)
        
        return results
    
    def list_all(self, collection: str) -> List[Dict[str, Any]]:
        """List all records in collection"""
        collection_data = self._load_collection(collection)
        return collection_data.get("data", [])
    
    def backup(self, backup_dir: Path, prefix: str = "") -> str:
        """Create backup of all data"""
        import shutil
        from datetime import datetime
        
        backup_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{prefix}_backup_{timestamp}" if prefix else f"backup_{timestamp}"
        backup_path = backup_dir / backup_name
        
        shutil.copytree(self.data_dir, backup_path)
        logger.info(f"Backup created: {backup_path}")
        
        return str(backup_path)
    
    def restore(self, backup_path: Path) -> bool:
        """Restore from backup"""
        import shutil
        
        try:
            if self.data_dir.exists():
                shutil.rmtree(self.data_dir)
            shutil.copytree(backup_path, self.data_dir)
            logger.info(f"Restored from backup: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Restore failed: {e}")
            return False

class DatabaseManager:
    """Main database manager"""
    
    def __init__(self, adapter: DatabaseAdapter):
        """
        Initialize database manager
        
        Args:
            adapter: Database adapter instance
        """
        self.adapter = adapter
    
    def __getattr__(self, name: str):
        """Delegate to adapter"""
        return getattr(self.adapter, name)
