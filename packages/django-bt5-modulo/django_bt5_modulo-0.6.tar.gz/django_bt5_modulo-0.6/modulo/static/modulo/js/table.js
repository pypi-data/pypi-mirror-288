// import sheet from "/static/modulo/plugins/bootstrap/dist/css/bootstrap.min.css" ;

export default class TableView extends HTMLElement {

    constructor() {
        super();
        this.attachShadow({mode: "open"});

    }

    async connectedCallback() {
        // document.adoptedStyleSheets = [sheet];
        // this.shadowRoot.adoptedStyleSheets = [sheet];
        this.shadowRoot.innerHTML = `
            <link rel="stylesheet" href="/static/modulo/plugins/bootstrap/dist/css/bootstrap.min.css"
            <div class="table-responsive">
                <table>
                <thead></thead>
                <tbody></tbody>
                </table>
            </div>
        `;
    }

    /**
     *
     * @param data {{}}
     */

    set data(data) {
        const table = this.shadowRoot.querySelector('table');
        table.classList.add('table');
        table.classList.add('table-bordered');
        const tableBody = this.shadowRoot.querySelector('tbody');
        const tableHead = this.shadowRoot.querySelector('thead');
        const tr = document.createElement('tr');
        const heads = data.headers.map(headData => {
            const colum = document.createElement('th');
            colum.textContent = headData
            return colum
        })
        tr.append(...heads);
        tableHead.append(tr)
        const rows = data.rows.map(rowData => {
            const row = document.createElement('tr');
            row.setAttribute('data-pk', rowData.id)
            for (let key in rowData) {
                if (key !== 'id') {
                    const td = document.createElement('td');
                    td.textContent = rowData[key]
                    td.classList.add('text-center')
                    row.append(td)
                }
            }
            // colum.textContent = headData
            return row
        })
        tableBody.append(...rows)
    }
}