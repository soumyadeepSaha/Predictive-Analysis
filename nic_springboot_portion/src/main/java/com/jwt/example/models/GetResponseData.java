package com.jwt.example.models;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.sql.Timestamp;
import java.util.Map;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class GetResponseData {
    private String requestKey;
    private Map<String,Object> resultSet;
    private Timestamp lastAccessedOn;
    private int noOfTimeAccessed;
}
