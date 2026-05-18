<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>전체 병상 현황</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        h1 { color: #1565c0; text-align: center; }
        .summary { text-align: center; margin: 10px 0 20px 0; color: #555; }
        table { width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        th { background-color: #1565c0; color: white; padding: 12px; text-align: center; }
        td { padding: 10px; text-align: center; border-bottom: 1px solid #eee; }
        tr:hover { background-color: #f0f4ff; }
        .available { color: #2e7d32; font-weight: bold; }
        .none { color: #aaa; }
        .nav { text-align: center; margin-bottom: 20px; }
        .nav a { margin: 0 10px; color: #1565c0; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <h1>🏥 전체 병상 현황</h1>
    <div class="nav">
        <a href="/">가용병상 현황</a>
        <a href="/beds">전체 병상 현황</a>
    </div>
    <div class="summary">전체 병원: ${beds.size()}개</div>
    <table>
        <tr>
            <th>병원명</th>
            <th>주소</th>
            <th>응급실 전화</th>
            <th>일반병상</th>
            <th>수술실</th>
            <th>중환자실</th>
            <th>신생아중환자실</th>
            <th>일반입원실</th>
        </tr>
        <c:forEach var="b" items="${beds}">
        <tr>
            <td>${b.duty_name}</td>
            <td>${b.duty_addr}</td>
            <td>${b.duty_tel3}</td>
            <td class="${b.hv_ec > 0 ? 'available' : 'none'}">${b.hv_ec}</td>
            <td class="${b.hv_oc > 0 ? 'available' : 'none'}">${b.hv_oc}</td>
            <td class="${b.hv_cc > 0 ? 'available' : 'none'}">${b.hv_cc}</td>
            <td class="${b.hv_ncc > 0 ? 'available' : 'none'}">${b.hv_ncc}</td>
            <td class="${b.hv_gc > 0 ? 'available' : 'none'}">${b.hv_gc}</td>
        </tr>
        </c:forEach>
    </table>
</body>
</html>