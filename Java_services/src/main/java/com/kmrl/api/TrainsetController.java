package com.kmrl.api;

import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import java.util.Map;

@RestController
@RequestMapping("/api/trainsets")
public class TrainsetController {

    private final RestTemplate restTemplate = new RestTemplate();

    @GetMapping("/ranked")
    public Object getRankedTrainsets() {
        String pythonUrl = "http://127.0.0.1:5000/api/ranked"; // Python must expose this
        return restTemplate.getForObject(pythonUrl, Object.class);
    }

    @PostMapping("/simulate")
    public Object simulate(@RequestBody Map<String, String> payload) {
        String pythonUrl = "http://127.0.0.1:5000/api/simulate";
        return restTemplate.postForObject(pythonUrl, payload, Object.class);
    }
}
