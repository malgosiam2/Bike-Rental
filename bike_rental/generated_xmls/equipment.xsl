<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/Equipment">
        <html>
            <head>
                <style>
                    table {
                        width: 100%;
                        border-collapse: collapse;
                        margin-bottom: 40px;
                    }
                    th, td {
                        border: 1px solid #ddd;
                        padding: 8px;
                        text-align: left;
                    }

                    th {
                        background-color: #4CAF50;  /* Zielony kolor dla nagłówków */
                        color: white;
                    }

                    tr:nth-child(even) {
                        background-color: #e7f7e0;  /* Jasno szare tło co drugiego wiersza */
                    }

                    tr:nth-child(odd) {
                        background-color: #ffffff;  /* Białe tło dla nieparzystych wierszy */
                    }

                    table.accessories tr:nth-child(even) {
                        background-color: #e7f7e0;  /* Jasno zielony tło dla co drugiego wiersza */
                    }

                    table.accessories tr:nth-child(odd) {
                        background-color: #ffffff;  /* Białe tło dla nieparzystych wierszy */
                    }

                    h1 {
                        text-align: center;
                        color: #333;
                        font-family: Arial, sans-serif;
                    }

                    h2 {
                        color: #4CAF50;
                    }
                </style>
            </head>
            <body>
                <h1>Equipment List</h1>

                <h2>Bikes</h2>
                <table>
                    <tr>
                        <th>Bike Type</th>
                        <th>Gear Number</th>
                        <th>Usage</th>
                        <th>Weight</th>
                        <th>Wheel Size (cm)</th>
                        <th>Price per Day</th>
                        <th>Brand</th>
                        <th>Quantity</th>
                    </tr>
                    <xsl:for-each select="bikes/bike">
                        <xsl:sort select="bike_type" order="ascending"/>
                        <tr>
                            <td><xsl:value-of select="bike_type"/></td>
                            <td><xsl:value-of select="gear_num"/></td>
                            <td><xsl:value-of select="usage"/></td>
                            <td><xsl:value-of select="weight"/></td>
                            <td><xsl:value-of select="wheel_size_cm"/></td>
                            <td><xsl:value-of select="price_for_one_day"/></td>
                            <td><xsl:value-of select="brand"/></td>
                            <td><xsl:value-of select="quantity"/></td>
                        </tr>
                    </xsl:for-each>
                </table>

                <h2>Accessories</h2>
                <table class="accessories">
                    <tr>
                        <th>Accessory Type</th>
                        <th>Price per Day</th>
                        <th>Brand</th>
                        <th>Quantity</th>
                    </tr>
                    <xsl:for-each select="accessories/accessory">
                        <xsl:sort select="accessory_type" order="ascending"/>
                        <tr>
                            <td><xsl:value-of select="accessory_type"/></td>
                            <td><xsl:value-of select="price_for_one_day"/></td>
                            <td><xsl:value-of select="brand"/></td>
                            <td><xsl:value-of select="quantity"/></td>
                        </tr>
                    </xsl:for-each>
                </table>
            </body>
        </html>
    </xsl:template>

</xsl:stylesheet>
