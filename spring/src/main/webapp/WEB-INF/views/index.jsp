<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>실시간 응급실 가용병상 모니터링</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        h1 { color: #d32f2f; text-align: center; }
        .nav { text-align: center; margin-bottom: 20px; }
        .nav a { margin: 0 10px; color: #d32f2f; text-decoration: none; font-weight: bold; }
        .stats { display: flex; justify-content: center; gap: 20px; margin: 20px 0; }
        .card { background: white; border-radius: 10px; padding: 20px 40px; text-align: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .card .num { font-size: 2em; font-weight: bold; color: #d32f2f; }
        .card .label { color: #777; font-size: 0.9em; margin-top: 4px; }
        .update-info { text-align: center; color: #888; margin-bottom: 15px; font-size: 0.9em; }
        .countdown { color: #d32f2f; font-weight: bold; }
        .filters { display: flex; justify-content: center; gap: 10px; margin-bottom: 15px; flex-wrap: wrap; }
        .filters select, .filters input {
            padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px;
            font-size: 0.95em; outline: none;
        }
        .filters input { width: 200px; }
        table { width: 100%; border-collapse: collapse; background: white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        th { background-color: #d32f2f; color: white; padding: 12px; text-align: center; cursor: pointer; }
        th:hover { background-color: #b71c1c; }
        td { padding: 10px; text-align: center; border-bottom: 1px solid #eee; }
        tr:hover { background-color: #fff3f3; }
        .available { color: #2e7d32; font-weight: bold; }
        .none { color: #aaa; }
        .sort-icon { margin-left: 5px; font-size: 0.8em; }
        #noResult { text-align: center; padding: 30px; color: #aaa; display: none; }
    </style>
</head>
<body>
    <h1>🚑 실시간 응급실 가용병상 모니터링</h1>
    <div class="nav">
        <a href="/emergencyroom/">가용병상 현황</a>
        <a href="/emergencyroom/beds">전체 병상 현황</a>
    </div>
    <div class="stats">
        <div class="card">
            <div class="num" id="totalHospitals">0</div>
            <div class="label">가용병상 보유 병원 수</div>
        </div>
        <div class="card">
            <div class="num" id="totalBeds">0</div>
            <div class="label">총 가용 일반병상 수</div>
        </div>
        <div class="card">
            <div class="num" id="totalICU">0</div>
            <div class="label">총 가용 중환자실 수</div>
        </div>
    </div>
    <div class="update-info">
        마지막 업데이트: <span id="lastUpdate"></span> &nbsp;|&nbsp;
        다음 업데이트까지: <span class="countdown" id="countdown"></span>
    </div>
    <div class="filters">
        <select id="regionFilter" onchange="applyFilters()">
            <option value="">전체 지역</option>
        </select>
        <input type="text" id="searchInput" placeholder="🔍 병원명 검색" oninput="applyFilters()">
    </div>
    <table id="hospitalTable">
        <thead>
            <tr>
                <th onclick="sortTable(0)">병원명 <span class="sort-icon">↕</span></th>
                <th>주소</th>
                <th>응급실 전화</th>
                <th onclick="sortTable(3)">일반병상 <span class="sort-icon">↕</span></th>
                <th onclick="sortTable(4)">수술실 <span class="sort-icon">↕</span></th>
                <th onclick="sortTable(5)">중환자실 <span class="sort-icon">↕</span></th>
                <th onclick="sortTable(6)">신생아중환자실 <span class="sort-icon">↕</span></th>
                <th onclick="sortTable(7)">일반입원실 <span class="sort-icon">↕</span></th>
            </tr>
        </thead>
        <tbody id="tableBody">
            <c:forEach var="h" items="${hospitals}">
            <tr>
                <td>${h.duty_name}</td>
                <td>${h.duty_addr}</td>
                <td>${h.duty_tel3}</td>
                <td class="${h.hv_ec > 0 ? 'available' : 'none'}">${h.hv_ec}</td>
                <td class="${h.hv_oc > 0 ? 'available' : 'none'}">${h.hv_oc}</td>
                <td class="${h.hv_cc > 0 ? 'available' : 'none'}">${h.hv_cc}</td>
                <td class="${h.hv_ncc > 0 ? 'available' : 'none'}">${h.hv_ncc}</td>
                <td class="${h.hv_gc > 0 ? 'available' : 'none'}">${h.hv_gc}</td>
            </tr>
            </c:forEach>
        </tbody>
    </table>
    <div id="noResult">검색 결과가 없습니다.</div>
    <script>
        const allRows = Array.from(document.querySelectorAll('#tableBody tr'));
        const now = new Date();
        document.getElementById('lastUpdate').textContent = now.toLocaleString('ko-KR');
        let totalBeds = 0, totalICU = 0;
        allRows.forEach(row => {
            const cells = row.querySelectorAll('td');
            totalBeds += parseInt(cells[3].textContent) || 0;
            totalICU  += parseInt(cells[5].textContent) || 0;
        });
        document.getElementById('totalHospitals').textContent = allRows.length;
        document.getElementById('totalBeds').textContent = totalBeds;
        document.getElementById('totalICU').textContent = totalICU;
        const regions = new Set();
        allRows.forEach(row => {
            const addr = row.querySelectorAll('td')[1].textContent.trim();
            const region = addr.split(' ')[0];
            if (region) regions.add(region);
        });
        const regionSelect = document.getElementById('regionFilter');
        [...regions].sort().forEach(r => {
            const opt = document.createElement('option');
            opt.value = r; opt.textContent = r;
            regionSelect.appendChild(opt);
        });
        function applyFilters() {
            const region = document.getElementById('regionFilter').value;
            const keyword = document.getElementById('searchInput').value.toLowerCase();
            const tbody = document.getElementById('tableBody');
            tbody.innerHTML = '';
            let count = 0;
            allRows.forEach(row => {
                const cells = row.querySelectorAll('td');
                const name = cells[0].textContent.toLowerCase();
                const addr = cells[1].textContent;
                const matchRegion = !region || addr.startsWith(region);
                const matchKeyword = !keyword || name.includes(keyword);
                if (matchRegion && matchKeyword) {
                    tbody.appendChild(row);
                    count++;
                }
            });
            document.getElementById('noResult').style.display = count === 0 ? 'block' : 'none';
        }
        let sortDir = {};
        function sortTable(colIdx) {
            sortDir[colIdx] = !sortDir[colIdx];
            const tbody = document.getElementById('tableBody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            rows.sort((a, b) => {
                const aVal = a.querySelectorAll('td')[colIdx].textContent.trim();
                const bVal = b.querySelectorAll('td')[colIdx].textContent.trim();
                const aNum = parseFloat(aVal), bNum = parseFloat(bVal);
                if (!isNaN(aNum) && !isNaN(bNum)) {
                    return sortDir[colIdx] ? bNum - aNum : aNum - bNum;
                }
                return sortDir[colIdx] ? bVal.localeCompare(aVal) : aVal.localeCompare(bVal);
            });
            rows.forEach(r => tbody.appendChild(r));
        }
        let seconds = 300;
        function updateCountdown() {
            const m = Math.floor(seconds / 60);
            const s = seconds % 60;
            const sStr = s < 10 ? '0' + s : '' + s;
            document.getElementById('countdown').textContent = m + '분 ' + sStr + '초';
            if (seconds <= 0) location.reload();
            else seconds--;
        }
        updateCountdown();
        setInterval(updateCountdown, 1000);
    </script>
</body>
</html>