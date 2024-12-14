import { RedirectBtn } from "./redirect_btn";
import { dynamicRoutes } from "../../routes/routes";

export function Table({colName, dataName, rowData, where}) {
    return (
        <table class="table mt-4 text-center">
        <thead>
            <tr>
            {colName.map((col, index) => (
                <th scope="col" key={index}>{col}</th>
            ))}
            <th></th>
            </tr>
        </thead>
        <tbody>
            {rowData.map((data) => (
            <tr scope="row" key={data[dataName[0]]}>
                {dataName.map((name) => {
                    console.log(name);
                    if (name === "IsActive") {
                        return (<td scope="col" key={`${data[dataName[0]]}-${name}`}>{data["IsActive"] === 0 ? "✅" : "❌"}</td>)
                    } else {
                        return (<td scope="col" key={`${data[dataName[0]]}-${name}`}>{data[name]}</td>)
                    }
                })}
                <td>
                    {/* btn */}
                    {/* dynamicRoutes.busDetail(data[colName[0]]) */}
                    <RedirectBtn
                        redirectTo={dynamicRoutes.detail(where, data[dataName[0]])}
                        btnContent="Modify"
                        btnClass="btn btn-secondary cus-font"
                    />
                </td>
            </tr>
            ))}
        </tbody>
        </table>
    );
}
