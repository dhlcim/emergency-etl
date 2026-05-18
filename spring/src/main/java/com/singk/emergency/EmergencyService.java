package com.singk.emergency;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import com.fasterxml.jackson.databind.ObjectMapper;

public class EmergencyService {

    private static final String FASTAPI_URL = "http://127.0.0.1:8000";
    private final ObjectMapper objectMapper = new ObjectMapper();

    public List<Map<String, Object>> getAvailableBeds() {
        return callApi("/beds/available");
    }

    public List<Map<String, Object>> getAllBeds() {
        return callApi("/beds");
    }

    public List<Map<String, Object>> getAllHospitals() {
        return callApi("/hospitals");
    }

    @SuppressWarnings("unchecked")
    private List<Map<String, Object>> callApi(String endpoint) {
        List<Map<String, Object>> result = new ArrayList<>();
        try {
            URL url = new URL(FASTAPI_URL + endpoint);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setRequestProperty("Accept", "application/json");

            BufferedReader br = new BufferedReader(
                new InputStreamReader(conn.getInputStream(), "UTF-8"));
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = br.readLine()) != null) {
                sb.append(line);
            }
            br.close();

            result = objectMapper.readValue(sb.toString(), List.class);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return result;
    }
}