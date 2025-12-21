import React, { useState, useEffect } from "react";
import { getTransactions } from "../../services/transaction";
import styles from "./Transaction.module.css";

export default function Transaction() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedType, setSelectedType] = useState("All Types");
  const [selectedCategory, setSelectedCategory] = useState("All Categories");
  const [fromDate, setFromDate] = useState("");
  const [toDate, setToDate] = useState("");
  const [entriesPerPage, setEntriesPerPage] = useState("10");

  const [transactions, setTransactions] = useState([]);

  const fetchTransactions = async () => {
    try {
      const filters = {};
      if (fromDate) filters.from_date = fromDate;
      if (toDate) filters.to_date = toDate;

      const payload = {
        filters: Object.keys(filters).length > 0 ? filters : {},
        limit: parseInt(entriesPerPage),
        offset: 0,
      };

      const data = await getTransactions(
        "d9495332-1507-5738-94e3-51376d3173c1",
        payload
      );
      // Assuming the API returns the list directly or in a property. 
      // Adjust based on actual API response structure.
      setTransactions(data.transactions || (Array.isArray(data) ? data : []));
    } catch (error) {
      console.error("Failed to fetch transactions:", error);
    }
  };

  useEffect(() => {
    fetchTransactions();
  }, [fromDate, toDate, entriesPerPage]);

  const getCategoryIcon = (budgetName) => {
    return budgetName ? budgetName.charAt(0).toUpperCase() : "?";
  };

  const formatAmount = (amount) => {
    const formatted = Math.abs(amount).toFixed(2);
    return `$${formatted}`;
  };

  const handleClearDates = () => {
    setFromDate("");
    setToDate("");
  };

  const filteredTransactions = transactions.filter((t) => {
    const matchesSearch =
      t.transaction_info.toLowerCase().includes(searchQuery.toLowerCase()) ||
      t.budget_name.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesType =
      selectedType === "All Types" ||
      t.transaction_type.toLowerCase() === selectedType.toLowerCase();

    const matchesCategory =
      selectedCategory === "All Categories" ||
      t.budget_name === selectedCategory;

    // Date filtering is now handled by the API
    return matchesSearch && matchesType && matchesCategory;
  });

  const displayedTransactions = filteredTransactions;

  return (
    <div className={styles.container}>
      {/* Header */}
      <div className={styles.header}>
        <h1 className={styles.title}>Transactions</h1>
        <button className={styles.btnAdd}>
          <span className={styles.icon}>+</span>
          Add Transaction
        </button>
      </div>

      {/* Filters */}
      <div className={styles.filtersSection}>
        <div className={styles.filterRow}>
          <div className={styles.searchBox}>
            <input
              type="text"
              placeholder="Search transactions..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className={styles.searchInput}
            />
            <span className={styles.searchIcon}>🔍</span>
          </div>

          <select
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
            className={styles.select}
          >
            <option>All Types</option>
            <option>Income</option>
            <option>Expense</option>
          </select>

          <div className={styles.categoryGroup}>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className={styles.select}
            >
              <option>All Categories</option>
              <option>Utilities</option>
              <option>Transport</option>
              <option>Groceries</option>
              <option>Shopping</option>
              <option>Medical</option>
              <option>Miscellaneous</option>
              <option>Rent</option>
            </select>
          </div>

          <div className={styles.dateRow}>
            <div className={styles.dateInput}>
              <input
                type={fromDate ? "date" : "text"}
                placeholder="From Date"
                value={fromDate}
                onChange={(e) => setFromDate(e.target.value)}
                onFocus={(e) => e.target.type = 'date'}
                onBlur={(e) => !e.target.value && (e.target.type = 'text')}
                className={styles.dateField}
              />
            </div>

            <div className={styles.dateInput}>
              <input
                type={toDate ? "date" : "text"}
                placeholder="To Date"
                value={toDate}
                onChange={(e) => setToDate(e.target.value)}
                onFocus={(e) => e.target.type = 'date'}
                onBlur={(e) => !e.target.value && (e.target.type = 'text')}
                className={styles.dateField}
              />
            </div>
          </div>

          <button onClick={handleClearDates} className={styles.btnClear}>
            Clear Dates
          </button>
        </div>
      </div>

      {/* Table header + controls */}
      <div className={styles.tableSection}>
        <div className={styles.tableHeader}>
          <h2 className={styles.sectionTitle}>Recent Transactions</h2>
          <div className={styles.entriesControl}>
            <span>Show</span>
            <select
              value={entriesPerPage}
              onChange={(e) => setEntriesPerPage(e.target.value)}
              className={styles.entriesSelect}
            >
              <option>10</option>
              <option>25</option>
              <option>50</option>
              <option>100</option>
            </select>
            <span>entries</span>
          </div>
        </div>

        <div className={styles.tableWrapper}>
          <table className={styles.table}>
            <thead>
              <tr>
                <th>Category</th>
                <th>Description</th>
                <th>Date</th>
                <th>Type</th>
                <th>Amount</th>
                <th style={{ textAlign: "center" }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {displayedTransactions.map((t) => (
                <tr key={t.transaction_id}>
                  <td className={styles.tdCategory}>
                    <span className={styles.categoryIcon}>
                      {getCategoryIcon(t.budget_name)}
                    </span>
                    <span className={styles.categoryName}>{t.budget_name}</span>
                  </td>
                  <td className={styles.tdDescription}>{t.transaction_info}</td>
                  <td className={styles.tdDate}>{t.transaction_date}</td>
                  <td>
                    <span className={styles.typeBadge}>
                      {t.transaction_type.charAt(0).toUpperCase() +
                        t.transaction_type.slice(1)}
                    </span>
                  </td>
                  <td className={`${styles.amount} ${t.transaction_type === "expense" ? styles.negative : styles.positive}`}>
                    {formatAmount(t.transaction_amount, t.transaction_type)}
                  </td>
                  <td className={styles.tdActions}>
                    <button className={styles.actionBtn} title="Delete">🗑️</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
