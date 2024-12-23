SELECT p.ProductID, p.ProductName, SUM(s.Quantity) AS TotalSold
FROM products p
JOIN sales s ON p.ProductID = s.ProductID
GROUP BY p.ProductID, p.ProductName
ORDER BY TotalSold DESC
LIMIT 10;

