package com.jwt.example.entities;


import com.fasterxml.jackson.databind.annotation.JsonNaming;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.redis.core.RedisHash;
import java.io.Serializable;
import java.util.ArrayList;


@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
//@JsonNaming()
//@RedisHash("PredictionData")
public class PredictionData {
    private String category;
    private String subCategory;
    private int expectedPeriodInMonth;
    private int outDataPattern;
    private ArrayList<String> demandDate;
    private ArrayList<Integer> demandQty;
    private int analysisYear;
}
