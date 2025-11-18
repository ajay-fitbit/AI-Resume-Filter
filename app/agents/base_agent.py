"""
Base Agent Class for Multi-Agent System

All agents inherit from this base class to ensure consistent interface
"""

from typing import Dict, Any, List
from datetime import datetime
import time

class BaseAgent:
    """Base class for all agents in the system"""
    
    def __init__(self, name: str):
        self.name = name
        self.execution_logs = []
        
    def log(self, message: str, level: str = "info"):
        """Log agent activity"""
        log_entry = {
            "agent": self.name,
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message
        }
        self.execution_logs.append(log_entry)
        print(f"[{self.name}] {level.upper()}: {message}")
        
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution method - must be implemented by subclasses
        
        Args:
            input_data: Dictionary containing input for the agent
            
        Returns:
            Dictionary containing agent's output
        """
        raise NotImplementedError("Subclasses must implement execute()")
    
    def get_logs(self) -> List[Dict[str, Any]]:
        """Return execution logs"""
        return self.execution_logs
    
    def clear_logs(self):
        """Clear execution logs"""
        self.execution_logs = []
        
    def timed_execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute with timing information"""
        start_time = time.time()
        self.log(f"Starting execution")
        
        try:
            result = self.execute(input_data)
            execution_time = time.time() - start_time
            
            result['metadata'] = result.get('metadata', {})
            result['metadata']['execution_time'] = round(execution_time, 3)
            result['metadata']['agent_name'] = self.name
            
            self.log(f"Completed in {execution_time:.3f}s", "success")
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log(f"Failed after {execution_time:.3f}s: {str(e)}", "error")
            raise


class AgentState:
    """
    Shared state passed between agents in the workflow
    """
    def __init__(self):
        self.data = {}
        self.agent_results = {}
        self.errors = []
        
    def set(self, key: str, value: Any):
        """Set a value in shared state"""
        self.data[key] = value
        
    def get(self, key: str, default=None) -> Any:
        """Get a value from shared state"""
        return self.data.get(key, default)
    
    def add_agent_result(self, agent_name: str, result: Dict[str, Any]):
        """Store result from an agent"""
        self.agent_results[agent_name] = result
        
    def get_agent_result(self, agent_name: str) -> Dict[str, Any]:
        """Retrieve result from a specific agent"""
        return self.agent_results.get(agent_name, {})
    
    def add_error(self, agent_name: str, error: str):
        """Record an error"""
        self.errors.append({
            "agent": agent_name,
            "error": error,
            "timestamp": datetime.now().isoformat()
        })
        
    def has_errors(self) -> bool:
        """Check if any errors occurred"""
        return len(self.errors) > 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary"""
        return {
            "data": self.data,
            "agent_results": self.agent_results,
            "errors": self.errors
        }
