// Budget.js
import axios from "axios";
import { API_BASE_URL, API_VERSION } from "../env"


export const getBudgetOverview = async (userId, month) => {
  try {
    const response = await axios.get(`${API_BASE_URL}${API_VERSION}/budget/${userId}/overview`, {
      params: {
        month: month,
      },
    });

    return response.data;

  } catch (error) {
    console.error("Error fetching budget overview:", error);
    throw error;
  }
}

export const getBudgetDetails = async (userId, month) => {
  try {
    const response = await axios.get(`${API_BASE_URL}${API_VERSION}/budget/${userId}/details`, {
      params: {
        month: month,
      },
    });

    return response.data;

  } catch (error) {
    console.error("Error fetching budget details:", error);
    throw error;
  }
}

export const createBudgetService = async (userId, budgetData) => {
  try {
    const response = await axios.post(
      `${API_BASE_URL}${API_VERSION}/budget/${userId}/create`,
      budgetData
    );
    return response.data;

  } catch (error) {
    console.error("Error creating budget:", error);
    throw error;
  }
}