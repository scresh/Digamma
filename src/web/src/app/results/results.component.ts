import { Component, OnInit } from '@angular/core';
import {ResultsService} from "../results.service";
import {PageService} from "../page.service";
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.css']
})
export class ResultsComponent implements OnInit {

  results: any[];
  pager: any = {};
  resultOnPage: any[];

  setPage(page: number) {
        this.pager = this.pageService.getPager(this.results.length, page);
        this.resultOnPage = this.results.slice(this.pager.startIndex, this.pager.endIndex + 1);
  }

  getTorResults() {
    let queryType = this.route.snapshot.paramMap.get('type');

    if (queryType === 'tor'){
      let query = this.route.snapshot.paramMap.get('query');

      this.resultsService.getTorResults(query)
      .subscribe(data => {
        this.results = data["results"];
        this.setPage(1);
      });
    }else if(queryType === 'iot'){
    }
}

  constructor(private resultsService: ResultsService, private pageService: PageService, private route: ActivatedRoute)
  { }

  ngOnInit() {
    this.getTorResults();
  }

}
