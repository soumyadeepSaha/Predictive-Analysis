package com.jwt.example.models;


import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.ArrayList;


@Data
@AllArgsConstructor
@NoArgsConstructor
public class PushRequestData{
    private String category;
    private String subCategory;
    private int expectedPeriodInMonth;
    private int outDataPattern;
    private ArrayList<String> demandDate;
    private ArrayList<Integer> demandQty;
    private int analysisYear;
}
