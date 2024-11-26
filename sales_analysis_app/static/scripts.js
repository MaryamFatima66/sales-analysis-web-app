document.getElementById("submit-btn").addEventListener("click", function () {
    const data = {
        product_id: document.getElementById("product_id").value,
        product_name: document.getElementById("product_name").value,
        category: document.getElementById("category").value,
        sales_amount: parseFloat(document.getElementById("sales_amount").value),
        units_sold: parseInt(document.getElementById("units_sold").value),
        region: document.getElementById("region").value,
        customer_age: parseInt(document.getElementById("customer_age").value),
    };

    fetch("/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    })
        .then((response) => response.json())
        .then((result) => {
            alert(result.message);
            updateStats();
            updateChart();
        });
});

function updateStats() {
    fetch("/stats")
        .then((response) => response.json())
        .then((data) => {
            const statsContent = document.getElementById("stats-content");
            statsContent.innerHTML = `
                <p>Sales Mean: ${data.sales_mean}</p>
                <p>Sales Median: ${data.sales_median}</p>
                <p>Sales Std Dev: ${data.sales_std}</p>
                <p>Units Mean: ${data.units_mean}</p>
                <p>Age Mean: ${data.age_mean}</p>
            `;
        });
}

function updateChart() {
    document.querySelector("#chart img").src = "/chart?rand=" + Math.random();
}
