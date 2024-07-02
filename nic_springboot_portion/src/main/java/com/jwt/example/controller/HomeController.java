package com.jwt.example.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.jwt.example.entities.PredictionData;
import com.jwt.example.entities.PredictiveAnalysisResult;
import com.jwt.example.models.GetResponseData;
import com.jwt.example.models.PushRequestData;
//import com.jwt.example.services.PredictionDataService;
import com.jwt.example.services.RedisService;
import com.jwt.example.services.ResultDataService;
import com.jwt.example.services.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.Map;
import java.util.Objects;

@RestController
@RequestMapping("/home")
public class HomeController {
    @Autowired
    private UserService userService;
    @Autowired
    private ResultDataService resultDataService;
    @Autowired
    private RedisService redisService;
//    private PredictionDataService predictionDataService;

    @PostMapping("/data")
    public ResponseEntity saveNic(@RequestBody PredictionData data){
        try{
            // need to validate demand date

//            PredictionData result = predictionDataService.saveDataInRedis(data);
            String key = redisService.saveDataModel(data);
//            if(Objects.isNull(result)) return new ResponseEntity<>("Exception in Pushing Data",HttpStatus.INTERNAL_SERVER_ERROR);
            System.out.println(data);
            return new ResponseEntity<>(key,HttpStatus.CREATED);
        } catch (Exception ex){
            System.out.println(ex.getMessage());
            return new ResponseEntity<>("Exception in Pushing Data",HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @GetMapping("/data/{requestKey}")
    public ResponseEntity getDataFromDB(@PathVariable String requestKey){
        try{

            PredictiveAnalysisResult fetchedData = resultDataService.getResultData(requestKey);

            if(Objects.isNull(fetchedData)){
                return new ResponseEntity<>("No saved data found", HttpStatus.BAD_REQUEST);
            }
            Map<String,Object> parsedData =fetchedData.getResultSet();

            return new ResponseEntity<>(GetResponseData.builder()
                    .requestKey(fetchedData.getRequestKey())
                    .resultSet(parsedData)
                    .noOfTimeAccessed(fetchedData.getNoOfTimeAccessed())
                    .lastAccessedOn(fetchedData.getLastAccessedOn()).build(),HttpStatus.CREATED);
        } catch (Exception e){
            System.out.println(e.getMessage());
            return new ResponseEntity<>("Exception in Database fetching service",HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }


}
