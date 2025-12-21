// Budget.js
import axios from "axios";
import { API_BASE_URL, API_VERSION } from "../env"


export const getTransactions = async (userId, payload) => {
    try {
        const response = await axios.post(`${API_BASE_URL}${API_VERSION}/transactions/${userId}/details`, payload);

        return response.data;

    } catch (error) {
        console.error("Error fetching transactions:", error);
        throw error;
    }
}