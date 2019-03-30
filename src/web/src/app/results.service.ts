import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ResultsService {

  getTorResults() {
  return this.http.get("http://127.0.0.1:9000/searchTor?query=pluto");
}

  constructor(private http: HttpClient) { }
}
