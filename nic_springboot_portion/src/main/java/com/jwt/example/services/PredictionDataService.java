//package com.jwt.example.services;
//
//import com.jwt.example.entities.PredictionData;
//import com.jwt.example.models.PushRequestData;
//import com.jwt.example.repositories.PredictionDataRepo;
//import org.springframework.beans.factory.annotation.Autowired;
//import org.springframework.stereotype.Service;
//import java.util.Random;
//import java.util.UUID;
//
//@Service
//public class PredictionDataService {
//
//    @Autowired
//    private PredictionDataRepo predictionDataRepo;
//    @Autowired
//    private Random random;
//    @Autowired
//    private RedisService redisService;
//
//    public PredictionData saveDataInRedis(PushRequestData pushRequestData){
//
//        int randomNumber = 100 + random.nextInt(900);
//        String Key = UUID.randomUUID() + "OrgCode" + randomNumber;
//
//
//         RedisService.saveDataModel(Key,PredictionData.builder()
//                        .category(pushRequestData.getCategory())
//                        .subCategory(pushRequestData.getSubCategory())
//                        .expectedPeriodInMonth(pushRequestData.getExpectedPeriodInMonth())
//                        .outDataPattern(pushRequestData.getOutDataPattern())
//                        .demandDate(pushRequestData.getDemandDate())
//                        .demandQty(pushRequestData.getDemandQty())
//                        .analysisYear(pushRequestData.getAnalysisYear())
//                        .build());
//    }
//
//}
