import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
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
  browserType = 'ToR';

  constructor(public Searching: SearchingService, private route: ActivatedRoute) { }

  ngOnInit() {
  }

  setResultsPerPage(numberPerPage: number) {
    // const lastPerPage = this.resultsPerPage;
    this.resultsPerPage = numberPerPage;
    this.Searching.changePagination();
    this.Searching.setResultsPerPage(this.resultsPerPage);
    this.Searching.search(this.Searching.aim.what, 0, this.Searching.aim.howMuchPerPage);
    /* if (this.Searching.aim.whichPage !== 0) {
      const dest = Math.round((lastPerPage * (this.Searching.aim.whichPage + 1) / numberPerPage));
      this.Searching.search(this.Searching.aim.what, dest, this.Searching.aim.howMuchPerPage);
    } else {

    }
    */
  }
  setBrowserType(browserType: string) {
    this.browserType = browserType;
    this.Searching.setBrowserType(browserType);
  }
}
