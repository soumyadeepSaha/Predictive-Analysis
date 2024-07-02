package com.jwt.example.services;

import com.jwt.example.entities.PredictiveAnalysisResult;
import com.jwt.example.repositories.PredictiveAnalysisResultRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.sql.Timestamp;
import java.util.Objects;

@Service
public class ResultDataService {
    @Autowired
    PredictiveAnalysisResultRepo predictiveAnalysisResultRepo;
    public PredictiveAnalysisResult getResultData(String requestKey){
        PredictiveAnalysisResult predictiveAnalysisResult = predictiveAnalysisResultRepo.findByRequestKey(requestKey);
        if(Objects.isNull(predictiveAnalysisResult)) return null;
        predictiveAnalysisResult.setLastAccessedOn(new Timestamp(System.currentTimeMillis()));
        predictiveAnalysisResult.setNoOfTimeAccessed(predictiveAnalysisResult.getNoOfTimeAccessed()+1);
        return predictiveAnalysisResultRepo.save(predictiveAnalysisResult);
    }

}
