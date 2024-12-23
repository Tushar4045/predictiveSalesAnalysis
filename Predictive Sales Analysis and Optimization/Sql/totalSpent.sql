SELECT c.CustomerID, c.Name, SUM(s.TotalAmount) AS TotalSpent
FROM customers c
JOIN sales s ON c.CustomerID = s.CustomerID
GROUP BY c.CustomerID, c.Name
ORDER BY TotalSpent DESC
LIMIT 10;
