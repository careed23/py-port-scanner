<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Network Threat Dashboard</title>
    <style>
        body {
            background-color: #1a1a1a;
            color: #00ff00;
            font-family: 'Courier New', Courier, monospace;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            border: 1px solid #333;
            padding: 20px;
            box-shadow: 0 0 10px #00ff00;
        }
        h1 { text-align: center; text-transform: uppercase; border-bottom: 2px solid #00ff00; padding-bottom: 10px; }
        .meta { color: #888; margin-bottom: 20px; font-size: 0.9em; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #333; padding: 10px; text-align: left; }
        th { background-color: #003300; color: #fff; }
        tr:nth-child(even) { background-color: #0d0d0d; }
        .badge {
            background-color: #ff3333;
            color: white;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
        }
        .safe { color: #888; font-style: italic; }
    </style>
</head>
<body>

<div class="container">
    <h1>🛡️ SOC Scan Report</h1>

    <?php
    $file = 'scan_results.json';
    
    if (file_exists($file)) {
        $json = file_get_contents($file);
        $data = json_decode($json, true);
        
        echo "<div class='meta'>";
        echo "<strong>Target IP:</strong> " . htmlspecialchars($data['target']) . "<br>";
        echo "<strong>Scan Time:</strong> " . htmlspecialchars($data['scan_time']);
        echo "</div>";

        echo "<table>";
        echo "<tr><th>Port</th><th>Service</th><th>Status</th><th>Action Needed</th></tr>";
        
        foreach ($data['results'] as $row) {
            $port = $row['port'];
            $service = strtoupper($row['service']);
            
            // Basic Logic: Flag dangerous ports
            $action = "<span class='safe'>No Action</span>";
            if ($port == 21 || $port == 23 || $port == 80) {
                $action = "<span class='badge'>INVESTIGATE</span>";
            }

            echo "<tr>";
            echo "<td>" . $port . "</td>";
            echo "<td>" . $service . "</td>";
            echo "<td>OPEN</td>";
            echo "<td>" . $action . "</td>";
            echo "</tr>";
        }
        echo "</table>";
    } else {
        echo "<h2 style='color:red'>No Scan Data Found. Run scanner.py first!</h2>";
    }
    ?>
    
</div>

</body>
</html>
