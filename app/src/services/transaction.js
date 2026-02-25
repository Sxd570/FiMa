// Budget.js
import axios from "axios";
import { API_BASE_URL, API_VERSION } from "../env"


export const getTransactions = async (userId, params) => {
    try {
        const response = await axios.get(`${API_BASE_URL}${API_VERSION}/transactions/${userId}`, { params });

        return response.data;

    } catch (error) {
        console.error("Error fetching transactions:", error);
        throw error;
    }
}