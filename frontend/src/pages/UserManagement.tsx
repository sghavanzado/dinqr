import React, { useState, useEffect } from 'react';
import { TextField, Button, Container, Typography, Grid } from '@mui/material';
import { userService } from '../api/apiService'; // Correctly import userService

const UserManagement = () => {
  const [users, setUsers] = useState([]);
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    email: '',
    role: '',
    name: '',
    second_name: '',
    last_name: '',
    phone_number: '',
  });

  useEffect(() => {
    const fetchUsers = async () => {
      const usersData = await userService.getUsers(); // Use userService to fetch users
      setUsers(usersData);
    };
    fetchUsers();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await userService.createUser(formData); // Use userService to create a user
      const usersData = await userService.getUsers(); // Refresh the user list
      setUsers(usersData);
    } catch (error) {
      console.error('User creation failed', error);
    }
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        User Management
      </Typography>
      <form onSubmit={handleSubmit}>
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="username"
              label="Username"
              fullWidth
              value={formData.username}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="password"
              label="Password"
              type="password"
              fullWidth
              value={formData.password}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="email"
              label="Email"
              fullWidth
              value={formData.email}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="role"
              label="Role"
              fullWidth
              value={formData.role}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="name"
              label="Name"
              fullWidth
              value={formData.name}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              name="second_name"
              label="Second Name"
              fullWidth
              value={formData.second_name}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="last_name"
              label="Last Name"
              fullWidth
              value={formData.last_name}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              name="phone_number"
              label="Phone Number"
              fullWidth
              value={formData.phone_number}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12}>
            <Button type="submit" variant="contained" color="primary" fullWidth>
              Create User
            </Button>
          </Grid>
        </Grid>
      </form>
      <Typography variant="h5" gutterBottom>
        Existing Users
      </Typography>
      <ul>
        {users.map((user: any) => (
          <li key={user.id}>
            {user.username} - {user.email}
            <Button onClick={() => userService.deleteUser(user.id)}>Delete</Button>
          </li>
        ))}
      </ul>
    </Container>
  );
};

export default UserManagement;
