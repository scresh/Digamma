import { Router } from '@angular/router';
import { Component, OnInit, Input } from '@angular/core';
import { SearchingService } from '../searching-service.service';

@Component({
  selector: 'app-input-search',
  templateUrl: './input-search.component.html',
  styleUrls: ['./input-search.component.css']
})
export class InputSearchComponent implements OnInit {

  searchingText: String;

  constructor(public Searching: SearchingService, private router: Router) { }

  ngOnInit() {
  }

  search() {
    console.log(this.router.url);
    this.router.navigate(['/result/' + this.searchingText]);
  }

  setBrowserType(browserType: string) {
    this.Searching.setBrowserType(browserType);
  }
}
