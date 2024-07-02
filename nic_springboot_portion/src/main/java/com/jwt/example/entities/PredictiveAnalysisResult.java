package com.jwt.example.entities;

import io.hypersistence.utils.hibernate.type.json.JsonType;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.Type;
import java.sql.Timestamp;
import java.util.Map;



@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Table(name = "predictive_analysis_result")
public class PredictiveAnalysisResult {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "sl_no")
    private Long slNo;
    @Column(name = "request_key", nullable = false)
    private String requestKey;
    @Column(name = "result_set",columnDefinition = "jsonb")
    @Type(JsonType.class)
    private Map<String, Object> resultSet;
    @Column(name = "series_data",columnDefinition = "jsonb")
    @Type(JsonType.class)
    private Map<String, Object> seriesData;
    @Column(name = "no_of_time_accessed",nullable = false)
    private int noOfTimeAccessed=0;
    @Column(name = "last_accessed_on")
    private Timestamp lastAccessedOn;
    @Column(name = "last_accessed_from", length = 20)
    private String lastAccessedFrom;
    @Column(name = "is_block", nullable = false)
    private int isBlock = 0;
}
