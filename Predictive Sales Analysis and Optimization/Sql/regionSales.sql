SELECT c.Region, SUM(s.TotalAmount) AS RegionSales
FROM customers c
JOIN sales s ON c.CustomerID = s.CustomerID
GROUP BY c.Region
ORDER BY RegionSales DESC;


