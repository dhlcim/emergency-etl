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
        .summary { text-align: center; margin: 10px 0 20px 0; color: #555; }
        table { width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        th { background-color: #d32f2f; color: white; padding: 12px; text-align: center; }
        td { padding: 10px; text-align: center; border-bottom: 1px solid #eee; }
        tr:hover { background-color: #fff3f3; }
        .available { color: #2e7d32; font-weight: bold; }
        .none { color: #aaa; }
        .nav { text-align: center; margin-bottom: 20px; }
        .nav a { margin: 0 10px; color: #d32f2f; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <h1>🚑 실시간 응급실 가용병상 모니터링</h1>
    <div class="nav">
        <a href="/">가용병상 현황</a>
        <a href="/beds">전체 병상 현황</a>
    </div>
    <div class="summary">가용병상 보유 병원: ${hospitals.size()}개</div>
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
    </table>
</body>
</html>