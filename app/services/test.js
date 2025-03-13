    () => {
            let tables = document.querySelectorAll("#customers"); 
            let structuredData = [];

            tables.forEach((table, index) => {
                let rows = table.querySelectorAll("tbody tr");
                let section = index === 0 ? "Active Members" : "Previous Members"; // Determine section

                rows.forEach((row, rowIndex) => {
                    if (rowIndex === 0) return; // Skip the header row

                    let cells = row.querySelectorAll("td");
                    if (cells.length === 3) {
                        structuredData.push({
                            section: section,
                            role: cells[0].innerText.trim(),
                            memberName: cells[1].innerText.trim(),
                            email: cells[2].innerText.trim().replace("[at]", "@") // Convert email format
                        });
                    }
                });
            });

            return structuredData;
        }