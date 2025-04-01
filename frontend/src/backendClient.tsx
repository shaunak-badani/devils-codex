import axios from "axios";

const apiURL = import.meta.env.VITE_API_ENDPOINT;
console.log("apiURL : ", apiURL);

const backendClient = axios.create({
    baseURL: apiURL
});

export default backendClient;