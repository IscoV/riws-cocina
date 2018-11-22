import {Component, OnInit} from '@angular/core';
import {NgbCalendar, NgbDate} from '@ng-bootstrap/ng-bootstrap';
import {AppService} from './app.service';

interface Item {
    _id: string;
    _score: number;
    _source: {
        name: string,
        description: string,
        categories: string[],
        steps: string[],
        dinners: number,
        ingredients: string[],
        difficulty: number,
        time: number,
        url: string,
        meal_type: string,
        tags: string[],
        language: string,
        last_update: string,
    };
}

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
    today: NgbDate;
    fromDate: NgbDate;
    toDate: NgbDate;

    collapsed = true;
    page = 1;

    filter: { keywords?: string, dinners: number, difficulty: number, max_time?: any, last_update?: any } = {dinners: 1, difficulty: 5};
    found = {hits: [], total: 0};

    trackById = (obj) => obj._id;

    categories(item: Item) {
        return item._source.categories.slice(0, item._source.categories.length - 1);
    }

    difficulty(item: Item) {
        switch (item._source.difficulty) {
            case 1:
                return 'Muy Fácil';
            case 2:
                return 'Fácil';
            case 3:
                return 'Medio';
            case 4:
                return 'Difícil';
            case 5:
                return 'Muy Difícil';
        }
    }

    difficultyClass(item: Item) {
        switch (item._source.difficulty) {
            case 1:
                return 'badge-success';
            case 2:
                return 'badge-info';
            case 3:
                return 'badge-secondary';
            case 4:
                return 'badge-warning';
            case 5:
                return 'badge-danger';
        }
    }

    constructor(calendar: NgbCalendar, public service: AppService) {
        this.today = calendar.getToday();
        this.fromDate = calendar.getPrev(calendar.getToday(), 'y', 1);
        this.toDate = calendar.getToday();
        this.filter.last_update = {from: this.fromDate, to: this.toDate};
    }

    ngOnInit(): void {
    }

    search() {
        this.service.get(this.filter, this.page).subscribe(
            (data: { hits: { hits: Item[], total: number } }) => this.found = data.hits
        );
    }

}
