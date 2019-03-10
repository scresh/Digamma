import { Component, OnInit } from '@angular/core';
import { SearchingService } from '../searching-service.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.css']
})
export class ResultsComponent implements OnInit {

  browserType: {
    what: string,
    whichPage: number,
    howMuchPerPage: number,
    browserType: string,
    actualBrowserType: string
  };

  constructor(public Searching: SearchingService, private route: ActivatedRoute) {
    this.browserType = this.Searching.getSettings();

    this.route.params.subscribe(params => {
      if (params['page'] !== undefined && params['key'] !== undefined && params['browserType'] !== undefined) {
        console.log('page =' + params['page']);
        this.Searching.search(params['key'], Number(params['page']), this.Searching.aim.howMuchPerPage, params['browserType']);
      } else if (params['key'] !== undefined && params['browserType'] !== undefined) {
        this.route.params['key'] = params['key'];
        this.Searching.search(params['key'], 0, this.Searching.aim.howMuchPerPage, params['browserType']);
      }
    });

  }

  ngOnInit() {
  }

  changePage(numberPage) {
    this.Searching.search(this.Searching.aim.what, numberPage);
  }

  previousPage() {
    if (this.Searching.aim.whichPage !== 0) {
      this.Searching.search(this.Searching.aim.what, this.Searching.aim.whichPage - 1);
    }
  }

  nextPage() {
    if (this.Searching.aim.whichPage !== this.Searching.lastPage) {
      this.Searching.search(this.Searching.aim.what, this.Searching.aim.whichPage + 1);
    }
  }

}
