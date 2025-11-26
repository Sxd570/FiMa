import { useEffect, useState, useCallback } from "react";
import styles from "./Budget.module.css";
import { getBudgetOverview, getBudgetDetails, createBudgetService } from "../../services/budget";

export default function Budget() {
  const getCurrentMonth = () => {
    const now = new Date();
    const year = now.getFullYear();
    const month = `${now.getMonth() + 1}`.padStart(2, "0");
    return `${year}-${month}`;
  };

  const [selectedMonth, setSelectedMonth] = useState(getCurrentMonth());
  const [overviewData, setOverviewData] = useState({});
  const [budgets, setBudgets] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [newBudgetName, setNewBudgetName] = useState("");
  const [newBudgetLimit, setNewBudgetLimit] = useState("");
  const [errors, setErrors] = useState({
    name: false,
    limit: false,
  });

  const handleCreateBudget = async () => {
    const nameError = newBudgetName.trim() === "";
    const limitError = newBudgetLimit.trim() === "";

    if (nameError || limitError) {
      setErrors({
        name: nameError,
        limit: limitError,
      });
      return;
    }

    response_data = await createBudgetService("d9495332-1507-5738-94e3-51376d3173c1", {
      budget_name: newBudgetName,
      budget_limit: newBudgetLimit,
      budget_month: selectedMonth
    });

    setShowModal(false);
    setNewBudgetName("");
    setNewBudgetLimit("");
    setErrors({ name: false, limit: false });
  };


  const getBudgetOverviewData = useCallback(async () => {
    try {
      const data = await getBudgetOverview(
        "d9495332-1507-5738-94e3-51376d3173c1", 
        selectedMonth
      );
      setOverviewData(data);
    } catch (error) {
      console.error("Failed to fetch budget overview:", error);
    }
  }, [selectedMonth]);

  const getBudgetDetailData = useCallback(async () => {
    try {
      const data = await getBudgetDetails(
        "d9495332-1507-5738-94e3-51376d3173c1",
        selectedMonth
      );
      setBudgets(data.budget_details || []);
    } catch (error) {
      console.error("Failed to fetch budget details:", error);
    }
  }, [selectedMonth]); // Only recreate if selectedMonth changes

  useEffect(() => {
    getBudgetOverviewData();
    getBudgetDetailData();
  }, [selectedMonth]);

  const closeModal = () => {
    setShowModal(false);
    setNewBudgetName("");
    setNewBudgetLimit("");
    setErrors({ name: false, limit: false });
    getBudgetOverviewData();
    getBudgetDetailData();
  };

  const openModal = () => {
    setNewBudgetName("");
    setNewBudgetLimit("");
    setErrors({ name: false, limit: false });
    setShowModal(true);
  };


  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>Budget</h1>
        <div className={styles.headerControls}>
          <input
            type="month"
            value={selectedMonth}
            onChange={(e) => setSelectedMonth(e.target.value)}
            className={styles.monthPicker}
          />
          <button className={styles.addBtn} onClick={openModal}>
            + Add Budget
          </button>
        </div>
      </div>
      {showModal && (
        <div className={styles.modalBackdrop}>
          <div className={styles.modalBox}>
            <div className={styles.modalHeader}>
              <div>
                <h3 className={styles.modalTitle}>Create New Budget</h3>
                <p className={styles.modalSubtitle}>
                  For <b>{selectedMonth}</b>
                </p>
              </div>
              <span
                className={styles.modalClose}
                onClick={closeModal}
              >
                ×
              </span>
            </div>

            <div className={styles.modalBody}>
              <label className={styles.inputLabel}>Budget Name</label>
              <input
                className={`${styles.inputField} ${errors.name ? styles.inputError : ""}`}
                type="text"
                placeholder="e.g. Groceries"
                value={newBudgetName}
                onChange={(e) => {
                  setNewBudgetName(e.target.value);
                  setErrors((prev) => ({ ...prev, name: false }));
                }}
              />

              <label className={styles.inputLabel}>Budget Limit</label>
              <input
                className={`${styles.inputField} ${errors.limit ? styles.inputError : ""}`}
                type="number"
                placeholder="e.g. 50000"
                value={newBudgetLimit}
                onChange={(e) => {
                  setNewBudgetLimit(e.target.value);
                  setErrors((prev) => ({ ...prev, limit: false }));
                }}
              />

            </div>

            <div className={styles.modalFooter}>
              <button
                className={styles.createBtn}
                onClick={handleCreateBudget}
              >
                Create
              </button>
            </div>
          </div>
        </div>
      )}

      {/* OVERVIEW (Crypto-style metrics row) */}
      <div className={styles.metricsGrid}>
        <div className={styles.metricCard}>
          <span className={styles.metricLabel}>Total Budget</span>
          <div className={styles.metricValue}>${overviewData.budget_total_budget}</div>
        </div>

        <div className={styles.metricCard}>
          <span className={styles.metricLabel}>Total Spent</span>
          <div className={styles.metricValue}>${overviewData.budget_total_spent}</div>
        </div>

        <div className={styles.metricCard}>
          <span className={styles.metricLabel}>Remaining</span>
          <div className={styles.metricValue}>${overviewData.budget_remaining_amount}</div>
        </div>
      </div>

      <div className={styles.metricsGrid}>
        <div className={styles.metricCard}>
          <span className={styles.metricLabel}>Near Limit</span>
          <div className={styles.metricValue}>{overviewData.budget_near_limit_count}</div>
        </div>

        <div className={styles.metricCard}>
          <span className={styles.metricLabel}>Over Limit</span>
          <div className={styles.metricValue}>{overviewData.budget_over_limit_count}</div>
        </div>

        <div className={styles.metricCard}>
          <span className={styles.metricLabel}>Percentage Spent</span>
          <div className={styles.metricValue}>{overviewData.budget_percentage_spent}%</div>
        </div>
      </div>
      {/* BUDGET CARDS - Crypto asset style */}
      <div className={styles.budgetWrapper}>
        <div className={styles.cardGrid}>
          {budgets.map((item) => {
            let barColor = styles.green;
            if (item.is_over_limit || item.budget_percentage_spent >= 100)
              barColor = styles.red;
            else if (item.is_limit_reached) barColor = styles.yellow;

            return (
              <div key={item.budget_id} className={styles.assetCard}>
                <div className={styles.cardTop}>
                  <div className={styles.cardTitleSection}>
                    <h3 className={styles.assetName}>{item.budget_name}</h3>
                    <span className={styles.remainingValue}>
                      ${item.budget_remaining_amount}
                    </span>
                  </div>
                  <div className={styles.progressBar}>
                    <div
                      className={`${styles.progressFill} ${barColor}`}
                      style={{ width: `${item.budget_percentage_spent}%` }}
                    ></div>
                  </div>
                </div>

                <div className={styles.cardBottom}>
                  <div className={styles.bottomItem}>
                    <span className={styles.bottomLabel}>Spent / Total</span>
                    <span className={styles.bottomValue}>
                      ${item.budget_spent_amount} / ${item.budget_allocated_amount}
                    </span>
                  </div>

                  <div className={styles.bottomItem}>
                    <span className={styles.bottomLabel}>Spent %</span>
                    <span className={styles.bottomValue}>
                      {item.budget_percentage_spent}%
                    </span>
                  </div>
                </div>
              </div>
            );
          })}

        </div>
      </div>
    </div>
  );
}
