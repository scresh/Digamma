import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MatSelectModule } from '@angular/material/select';
import { SearchingService } from '../searching-service.service';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

@Component({
  selector: 'app-result-search',
  templateUrl: './result-search.component.html',
  styleUrls: ['./result-search.component.css']
})
export class ResultSearchComponent implements OnInit {

  resultsPerPage = 40;

  constructor(public Searching: SearchingService) { }

  ngOnInit() {
  }

  setResultsPerPage(numberPerPage: number) {
    this.resultsPerPage = numberPerPage;
    this.Searching.setResultsPerPage(this.resultsPerPage);
    this.Searching.changePagination();
  }
}
