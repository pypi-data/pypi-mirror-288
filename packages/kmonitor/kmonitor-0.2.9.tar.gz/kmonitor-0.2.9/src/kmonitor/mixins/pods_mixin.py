from collections import OrderedDict

from ..utils.consts import KCt

class _PodsMixin:
  def __init__(self):
    super(_PodsMixin, self).__init__()
    return
  
  def __get_pod_transition_time(self, pod_info):
    """
    Get the elapsed time since the pod transitioned to its current phase.
    """
    start_time = pod_info.status.conditions[-1].last_transition_time
    transition_time = self._get_elapsed(start_time)
    return transition_time
  
 
  
  def __get_pod_status(self, pod_name, namespace):
    try:
      pod = self.api.read_namespaced_pod(name=pod_name, namespace=namespace)
    except Exception as exc:
      self._handle_exception(exc)
      return None
    return self._check_pod_health(pod)
  
  
  def __list_pods(self, namespace=None):
    try:
      if namespace is None:
        ret = self.api.list_pod_for_all_namespaces(watch=False)
      else:
        ret = self.api.list_namespaced_pod(namespace, watch=False)
    except Exception as exc:
      self._handle_exception(exc)
      return None
    return ret.items
  
  
  def _check_pod_health(self, pod):
    try:
      # Fetch the specified pod      
      health_status = OrderedDict({
        "pod_name": pod.metadata.name,
        "status": "Success", 
        "messages": []
      })
      # Determine if the pod is in a loading or initializing state
      if pod.status.phase in ["Pending"]:
        initializing_status = False
        for condition in pod.status.conditions or []:
          if condition.type == "PodScheduled" and condition.status != "True":
            health_status["status"] = "Loading"
            health_status["messages"].append("Pod is scheduled but not running yet.")
            initializing_status = True
          elif condition.type in ["Initialized", "ContainersReady"] and condition.status != "True":
            health_status["status"] = "Initializing"
            health_status["messages"].append(f"Pod is initializing: {condition.type} is {condition.status}.")
            initializing_status = True

        if not initializing_status:
          # If the pod is pending but no specific initializing status was detected,
          # it could be waiting for resources or other conditions.
          health_status["status"] = "Loading"
          health_status["messages"].append("Pod is pending, waiting for resources or other conditions.")

        if self.__get_pod_transition_time(pod) > KCt.MAX_PENDING_TIME:
          health_status["status"] = "Warning"
          health_status["messages"].append(f"Pod has been pending for more than 5 minutes.")
        #end if transition time          
      #end if pod is pending
      elif pod.status.phase not in ["Running", "Succeeded"]:
        health_status["status"] = "Critical"
        health_status["messages"].append(f"Pod is in {pod.status.phase} phase.")
      # end if pod is not running or succeeded
      
      # Check container statuses if pod phase is Running
      if pod.status.phase == "Running":
        health_status["containers"] = {}
        for container_status in pod.status.container_statuses or []:
          container_name = container_status.name
          dct_container = {}
          # Check if container is ready 
          if not container_status.ready:
            health_status["status"] = "Warning"
            health_status["messages"].append(f"Container {container_status.name} is not ready.")
          # Check if container has restarted
          if container_status.restart_count > 0:
            health_status["status"] = "Warning"
            health_status["messages"].append(f"Container {container_status.name} restarted {container_status.restart_count} times.")
          # now compute running time for this pod containers                   
          run_info = container_status.state.running                  
          running_time = self._get_elapsed(run_info.started_at)
          hours, rem = divmod(running_time, 3600)
          minutes, seconds = divmod(rem, 60)
          # format elapsed time as a string        
          dct_container["started"] = run_info.started_at.strftime("%Y-%m-%d %H:%M:%S")
          dct_container["running_time"] = "{:0>2}:{:0>2}:{:0>2}".format(int(hours),int(minutes),int(seconds))
          if running_time < KCt.MIN_RUNNING_TIME:
            health_status["status"] = "Low warning"
            health_status["messages"].append(f"Low running time: Container {container_status.name} has been running for {dct_container['running_time']}.")
          else:
            health_status["status"] = "Success"
            health_status["messages"].append(f"Container {container_status.name} has been running for {dct_container['running_time']}.")  
          #end if running time
          health_status["containers"][container_name] = dct_container
        #end for container status
      #end if pod is running
    except Exception as e:
      self.P(f"An error occurred: {e}")
      health_status = {"status": "Error", "messages": [str(e)]}
    #end try
    return health_status  
  
  
  def __get_pod_by_name(self, pod_name):
    assert isinstance(pod_name, str), "`pod_name` must be a string"
    
    pods = self.list_pods()
    if pods is None:
      health_status = {"status": "Error", "messages": ["Unable to get pods"]}
    else:      
      found = None
      for p in pods:
        if p.metadata.name.startswith(pod_name):
          found = p
          break        
    return found
  
  
################################################################################################
# Public methods
################################################################################################
  

  def check_pod(self, namespace, pod_name):
    """
    Check the health of a pod by its name and namespace.
    
    Parameters
    ----------
    namespace : str
        The namespace where the pod is located.
    pod_name : str
        The name of the pod to check.
    
    Returns
    -------
      dict
        The health status of the pod.
    """
    return self.__get_pod_status(pod_name=pod_name, namespace=namespace)
  
  
  def check_pod_by_name(self, pod_name):
    """
    Check the health of a pod by its name.
    
    Parameters
    ----------
    pod_name : str
        The name of the pod to check.
    
    Returns
    -------
      dict
    """
    
    found_pod = self.__get_pod_by_name(pod_name)
    if found_pod is None:
      health_status = {"status": "Error", "messages": [f"Pod '{pod_name}' not found"]}
    else:
      health_status = self._check_pod_health(found_pod)
      #end if found
    return health_status
  
  
  def check_pods_by_names(self, lst_pod_names):
    """
    Check the health of a list of pods by their names.
    
    Parameters
    ----------
    lst_pod_names : list
        A list of pod names to check.
        
    Returns
    -------
      list
    """
    result = []
    for pod_name in lst_pod_names:
      status = self.check_pod_by_name(pod_name)
      result.append(status)
    return result
  
    
  def get_all_pods(self):
    """
    Get all pods in all namespaces.
    """
    lst_pods = self.__list_pods()
    return lst_pods


  def list_pods(self):
    """Get all pods in all namespaces."""
    return self.get_all_pods()
  


  def get_pods_by_namespace(self, namespace):
    """
    Get all pods in a specific namespace.
    """
    lst_pods = self.__list_pods(namespace=namespace)
    return lst_pods
  
  
  def get_all_pods_health(self):
    """
    Get the health status of all pods in all namespaces.
    """
    lst_pods = self.get_all_pods()
    result = []
    for pod in lst_pods:
      status = self._check_pod_health(pod)
      result.append(status)
    return result
  
  
  def delete_pods_from_namespace(self, base_name : str, namespace : str):
    """
    Delete all pods in a namespace that start with a specific name.
    
    Parameters
    ----------
    base_name : str
        The base name of the pods to delete.
    namespace : str
        The namespace where the pods are located.
    """
    assert isinstance(base_name, str), "`base_name` must be a string"
    assert isinstance(namespace, str), "`namespace` must be a string"
    
    pods = self.get_pods_by_namespace(namespace)
    if pods is None:
      self.P("No pods found in namespace {}".format(namespace)) 
      return
    #end if pods is None
    for pod in pods:
      if pod.metadata.name.startswith(base_name):
        self.P(f"Deleting pod {pod.metadata.name} in namespace {namespace}")
        res = self.api.delete_namespaced_pod(name=pod.metadata.name, namespace=namespace)
        if res is not None:
          creation_date = res.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")
          delete_date = res.metadata.deletion_timestamp.strftime("%Y-%m-%d %H:%M:%S")
          delta = res.metadata.deletion_timestamp - res.metadata.creation_timestamp
          lifetime_sec = (delta).total_seconds()
          elapsed_time = str(delta)
          msg = f"Pod {pod.metadata.name} deleted. Created: {creation_date}, Deleted: {delete_date}, Lifetime: {elapsed_time}."
          self.P(msg)
    #end for pod
    return
      