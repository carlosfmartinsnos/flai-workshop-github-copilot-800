import React, { useState, useEffect } from 'react';

function Users() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [teams, setTeams] = useState([]);
  const [editingUser, setEditingUser] = useState(null);
  const [showEditModal, setShowEditModal] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    team: '',
    total_points: 0
  });
  const [formErrors, setFormErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      const baseUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api`;
      
      try {
        // Fetch users
        const usersUrl = `${baseUrl}/users/`;
        console.log('Fetching users from:', usersUrl);
        const usersResponse = await fetch(usersUrl);
        if (!usersResponse.ok) {
          throw new Error(`HTTP error! status: ${usersResponse.status}`);
        }
        const usersData = await usersResponse.json();
        console.log('Users data received:', usersData);
        
        // Handle both paginated (.results) and plain array responses
        const usersArray = usersData.results || usersData;
        console.log('Processed users data:', usersArray);
        setUsers(Array.isArray(usersArray) ? usersArray : []);
        
        // Fetch teams
        const teamsUrl = `${baseUrl}/teams/`;
        console.log('Fetching teams from:', teamsUrl);
        const teamsResponse = await fetch(teamsUrl);
        if (teamsResponse.ok) {
          const teamsData = await teamsResponse.json();
          const teamsArray = teamsData.results || teamsData;
          setTeams(Array.isArray(teamsArray) ? teamsArray : []);
          console.log('Teams data received:', teamsArray);
        }
        
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Validation function
  const validateForm = () => {
    const errors = {};
    
    if (!formData.name || formData.name.trim() === '') {
      errors.name = 'Name is required';
    }
    
    if (!formData.email || formData.email.trim() === '') {
      errors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      errors.email = 'Invalid email format';
    }
    
    if (formData.team && !teams.find(t => t.name === formData.team)) {
      errors.team = 'Selected team does not exist';
    }
    
    if (formData.total_points < 0) {
      errors.total_points = 'Total points cannot be negative';
    }
    
    return Object.keys(errors).length > 0 ? errors : null;
  };

  // Handle edit button click
  const handleEditClick = (user) => {
    setEditingUser(user);
    setFormData({
      name: user.name || '',
      email: user.email || '',
      team: user.team || '',
      total_points: user.total_points || 0
    });
    setFormErrors({});
    setErrorMessage('');
    setShowEditModal(true);
  };

  // Handle form input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'total_points' ? parseInt(value) || 0 : value
    }));
    // Clear error for this field when user starts typing
    if (formErrors[name]) {
      setFormErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  // Handle save user
  const handleSaveUser = async () => {
    // Validate form
    const errors = validateForm();
    if (errors) {
      setFormErrors(errors);
      return;
    }
    
    setSubmitting(true);
    setErrorMessage('');
    
    try {
      const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/users/${editingUser.id}/`;
      console.log('Updating user at:', apiUrl);
      
      const response = await fetch(apiUrl, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }
      
      const updatedUser = await response.json();
      console.log('User updated successfully:', updatedUser);
      
      // Update users list
      setUsers(prev => prev.map(u => u.id === updatedUser.id ? updatedUser : u));
      
      // Show success message
      setSuccessMessage(`User "${updatedUser.name}" updated successfully!`);
      setTimeout(() => setSuccessMessage(''), 3000);
      
      // Close modal
      handleCloseModal();
    } catch (error) {
      console.error('Error updating user:', error);
      setErrorMessage(error.message);
    } finally {
      setSubmitting(false);
    }
  };

  // Handle close modal
  const handleCloseModal = () => {
    setShowEditModal(false);
    setEditingUser(null);
    setFormData({ name: '', email: '', team: '', total_points: 0 });
    setFormErrors({});
    setErrorMessage('');
  };

  if (loading) {
    return (
      <div className="container mt-5">
        <div className="text-center">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3">Loading users...</p>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="container mt-5">
        <div className="alert alert-danger" role="alert">
          <h4 className="alert-heading">Error!</h4>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-5">
      <div className="mb-4">
        <h2>👤 Users</h2>
        <p className="text-muted">All registered OctoFit members</p>
      </div>
      
      {/* Success Message */}
      {successMessage && (
        <div className="alert alert-success alert-dismissible fade show" role="alert">
          {successMessage}
          <button type="button" className="btn-close" onClick={() => setSuccessMessage('')}></button>
        </div>
      )}
      <div className="table-responsive">
        <table className="table table-hover">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Name</th>
              <th scope="col">Email</th>
              <th scope="col">Team</th>
              <th scope="col">Total Points</th>
              <th scope="col">Member Since</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.length > 0 ? (
              users.map((user) => (
                <tr key={user.id}>
                  <td><strong>{user.id}</strong></td>
                  <td><strong>{user.name}</strong></td>
                  <td>{user.email}</td>
                  <td>
                    {user.team ? (
                      <span className="badge bg-success">{user.team}</span>
                    ) : (
                      <span className="badge bg-secondary">No Team</span>
                    )}
                  </td>
                  <td><span className="badge bg-primary">{user.total_points}</span></td>
                  <td>{new Date(user.created_at).toLocaleDateString()}</td>
                  <td>
                    <button 
                      className="btn btn-sm btn-outline-primary"
                      onClick={() => handleEditClick(user)}
                    >
                      ✏️ Edit
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="7" className="text-center py-5">
                  <p className="text-muted mb-0">No users found</p>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      
      {/* Edit User Modal */}
      {showEditModal && (
        <div className="modal show d-block" tabIndex="-1" style={{backgroundColor: 'rgba(0,0,0,0.5)'}}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Edit User Profile</h5>
                <button type="button" className="btn-close" onClick={handleCloseModal} disabled={submitting}></button>
              </div>
              <div className="modal-body">
                {errorMessage && (
                  <div className="alert alert-danger" role="alert">
                    {errorMessage}
                  </div>
                )}
                
                <form>
                  {/* Name Field */}
                  <div className="mb-3">
                    <label htmlFor="name" className="form-label">Name <span className="text-danger">*</span></label>
                    <input
                      type="text"
                      className={`form-control ${formErrors.name ? 'is-invalid' : ''}`}
                      id="name"
                      name="name"
                      value={formData.name}
                      onChange={handleInputChange}
                      disabled={submitting}
                    />
                    {formErrors.name && (
                      <div className="invalid-feedback">{formErrors.name}</div>
                    )}
                  </div>
                  
                  {/* Email Field */}
                  <div className="mb-3">
                    <label htmlFor="email" className="form-label">Email <span className="text-danger">*</span></label>
                    <input
                      type="email"
                      className={`form-control ${formErrors.email ? 'is-invalid' : ''}`}
                      id="email"
                      name="email"
                      value={formData.email}
                      onChange={handleInputChange}
                      disabled={submitting}
                    />
                    {formErrors.email && (
                      <div className="invalid-feedback">{formErrors.email}</div>
                    )}
                  </div>
                  
                  {/* Team Field */}
                  <div className="mb-3">
                    <label htmlFor="team" className="form-label">Team</label>
                    <select
                      className={`form-select ${formErrors.team ? 'is-invalid' : ''}`}
                      id="team"
                      name="team"
                      value={formData.team}
                      onChange={handleInputChange}
                      disabled={submitting}
                    >
                      <option value="">No Team</option>
                      {teams.map((team) => (
                        <option key={team.id} value={team.name}>
                          {team.name}
                        </option>
                      ))}
                    </select>
                    {formErrors.team && (
                      <div className="invalid-feedback">{formErrors.team}</div>
                    )}
                  </div>
                  
                  {/* Total Points Field */}
                  <div className="mb-3">
                    <label htmlFor="total_points" className="form-label">Total Points</label>
                    <input
                      type="number"
                      className={`form-control ${formErrors.total_points ? 'is-invalid' : ''}`}
                      id="total_points"
                      name="total_points"
                      value={formData.total_points}
                      onChange={handleInputChange}
                      min="0"
                      disabled={submitting}
                    />
                    {formErrors.total_points && (
                      <div className="invalid-feedback">{formErrors.total_points}</div>
                    )}
                  </div>
                </form>
              </div>
              <div className="modal-footer">
                <button 
                  type="button" 
                  className="btn btn-secondary" 
                  onClick={handleCloseModal}
                  disabled={submitting}
                >
                  Cancel
                </button>
                <button 
                  type="button" 
                  className="btn btn-primary"
                  onClick={handleSaveUser}
                  disabled={submitting}
                >
                  {submitting ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                      Saving...
                    </>
                  ) : (
                    'Save Changes'
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Users;
