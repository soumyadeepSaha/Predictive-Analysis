package com.jwt.example.repositories;

import com.jwt.example.entities.PredictiveAnalysisResult;
import org.springframework.data.repository.CrudRepository;

public interface PredictiveAnalysisResultRepo extends CrudRepository<PredictiveAnalysisResult,Long> {
    public PredictiveAnalysisResult findByRequestKey(String requestKey);
}
