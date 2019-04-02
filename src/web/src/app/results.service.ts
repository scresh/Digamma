import { Injectable } from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ResultsService {
  getTorResults(query: string) {
    let params = new HttpParams().set("query", query);
    return this.http.get("http://127.0.0.1:9000/searchTor", {params: params});
}

  getTorPreview(page_id: string) {
    let params = new HttpParams().set("page_id", page_id);
    return this.http.get("http://127.0.0.1:9000/previewTor", {params: params});
}


getIoTResults(query: string) {
    let params = new HttpParams().set("query", query);
    return this.http.get("http://127.0.0.1:9000/searchIoT", {params: params});
}
  constructor(private http: HttpClient) { }
}
