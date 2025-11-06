import axios from 'axios';
import { API_BASE_URL, API_VERSION } from '../env';

export const loginService = async (
    email, 
    password
) => {
    try {
        const response = await axios.post(
            `${API_BASE_URL}${API_VERSION}/login`, 
            {
                user_email: email,
                password: password
            }
        );
        return response.data;
    } catch (error) {
        console.error('Login error', error);
        throw error;
    }
};


export const signUpService = async (
    username, 
    email, 
    password
) => {
    try {
        const response = await axios.post(
            `${API_BASE_URL}${API_VERSION}/signup`, 
            {
                user_name: username,
                user_email: email,
                password: password
            }
        );
        return response.data;
    } catch (error) {
        console.error('Signup error', error);
        throw error;
    }
};
