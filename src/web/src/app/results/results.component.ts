import { Component, OnInit } from '@angular/core';
import {ResultsService} from "../results.service";

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.css']
})
export class ResultsComponent implements OnInit {

  results = [];

  getTorResults() {
  this.resultsService.getTorResults()
    .subscribe(data => this.results = data["results"]);
}


  constructor(private resultsService: ResultsService) { }

  ngOnInit() {
    this.getTorResults();
  }

}
