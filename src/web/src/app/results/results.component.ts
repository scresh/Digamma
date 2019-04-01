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

  results = [];
  pager: any = {};
  resultOnPage = [];
  queryType = 'tor';

  setPage(page: number) {
        this.pager = this.pageService.getPager(this.results.length, page);
        this.resultOnPage = this.results.slice(this.pager.startIndex, this.pager.endIndex + 1);
  }

  getTorResults(query: string){
          this.resultsService.getTorResults(query)
      .subscribe(data => {
        this.results = data["results"];
        this.setPage(1);
      });
  }

  getIoTResults(query: string){
        this.resultsService.getIoTResults(query)
    .subscribe(data => {
      this.results = data["results"];
      this.setPage(1);
    });
}

  constructor(private resultsService: ResultsService, private pageService: PageService, private route: ActivatedRoute)
  { }

  ngOnInit() {
    let queryType = this.route.snapshot.paramMap.get('type');
    let query = this.route.snapshot.paramMap.get('query');

    if (queryType === 'tor'){
      this.queryType = 'tor';
      this.getTorResults(query);

    }else if(queryType === 'iot'){
      this.queryType = 'iot';
      this.getIoTResults(query);
    }

  }

}
