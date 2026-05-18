package com.singk.emergency;

import java.util.List;
import java.util.Map;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class EmergencyController {

    private final EmergencyService emergencyService = new EmergencyService();

    @GetMapping("/")
    public String index(Model model) {
        List<Map<String, Object>> hospitals = emergencyService.getAvailableBeds();
        model.addAttribute("hospitals", hospitals);
        return "index";
    }

    @GetMapping("/beds")
    public String beds(Model model) {
        List<Map<String, Object>> beds = emergencyService.getAllBeds();
        model.addAttribute("beds", beds);
        return "beds";
    }
}