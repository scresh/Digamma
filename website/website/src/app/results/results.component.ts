import { Component, OnInit } from '@angular/core';
import { SearchingService } from '../searching-service.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.css']
})
export class ResultsComponent implements OnInit {

  constructor(public Searching: SearchingService, private route: ActivatedRoute) {
    this.route.params.subscribe(params => {
      if (params['page'] !== undefined && params['key'] !== undefined) {
        console.log('page =' + params['page']);
        this.Searching.search(params['key'], Number(params['page']));
      } else if (params['key'] !== undefined) {
        this.route.params['key'] = params['key'];
        this.Searching.search(params['key'], 0);
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
