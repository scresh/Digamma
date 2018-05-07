import { Component, OnInit } from '@angular/core';
import { SearchingService } from "../searching-service.service";

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.css']
})
export class ResultsComponent implements OnInit {

  constructor(public Searching: SearchingService) {
  }

  ngOnInit() {
  }

  results1; results2; pagination = [
    {"active": true, "number": 1},
    {"active": false, "number": 2}
  ];
  page = {"number": 1};

}
