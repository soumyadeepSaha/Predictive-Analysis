package com.jwt.example.repositories;

import com.jwt.example.entities.PredictionData;
import org.springframework.data.repository.CrudRepository;

public interface PredictionDataRepo extends CrudRepository<PredictionData,String> {
}
