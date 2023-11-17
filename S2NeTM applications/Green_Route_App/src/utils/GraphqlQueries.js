import gql from "graphql-tag";

// const SENSORS = gql`
//   query Lat {
//     ioTEntities {
//       name
//       hasLocationLocationsAggregate {
//         node {
//           lat {
//             average
//           }
//           long {
//             average
//           }
//         }
//       }
//     }
//   }
// `;
// const LOCATIONS = gql`
// query IoTEntities {
//     ioTEntities {
//       name
//       hasLocationLocations {
//         lat
//         long  
//       }
//     }
//   }
// `;
const Entity_AQI = gql`
query Entity_AQI($spList: [String!]!, $partList: [String!]!, $aqiValues: [String!]!) {
  Entity_AQI(SP_List: $spList, PART_List: $partList, AQI_Values: $aqiValues) {
    name
    aqi
    point {
      lat
      long
    }
    pollutants {
      pollutant
      pol_aqi
      value
    }
  }
}
`
const PATH = gql`
mutation Path($spList: [String!]!, $partList: [String!]!, $aqiValues: [String!]!, $properAqi: [String!]!, $startPoint: user_point!, $endPoint: user_point!) {
  Path(SP_List: $spList, PART_List: $partList, AQI_Values: $aqiValues, proper_aqi: $properAqi, start_point: $startPoint, end_point: $endPoint) {
    idx
    lat
    long
    name
  }
}
`
export { Entity_AQI, PATH}