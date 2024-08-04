use super::peers::PyPeers;
use pyo3::{exceptions::PyException, prelude::*, types::PyDict};
use pythonize::{depythonize, pythonize};
use raftify::ClusterJoinTicket;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Serialize, Deserialize, Clone)]
#[pyclass(name = "ClusterJoinTicket")]
pub struct PyClusterJoinTicket {
    pub inner: ClusterJoinTicket,
}

#[pymethods]
impl PyClusterJoinTicket {
    #[new]
    pub fn new(reserved_id: u64, raft_addr: String, leader_addr: String, peers: PyPeers) -> Self {
        let peers = peers
            .inner
            .inner
            .iter()
            .map(|(id, peer)| (*id, peer.addr))
            .collect::<HashMap<_, _>>();

        PyClusterJoinTicket {
            inner: ClusterJoinTicket {
                reserved_id,
                raft_addr,
                leader_addr,
                peers,
            },
        }
    }

    pub fn __repr__(&self) -> String {
        format!("{:?}", self.inner)
    }

    pub fn get_reserved_id(&self) -> u64 {
        self.inner.reserved_id
    }

    pub fn to_dict(&self, py: Python) -> PyResult<PyObject> {
        pythonize(py, &self.inner).map_err(|e| PyException::new_err(e.to_string()))
    }

    #[staticmethod]
    pub fn from_dict(dict: &PyDict) -> PyResult<PyClusterJoinTicket> {
        let inner: ClusterJoinTicket =
            depythonize(dict).map_err(|e| PyException::new_err(e.to_string()))?;
        Ok(PyClusterJoinTicket { inner })
    }
}
