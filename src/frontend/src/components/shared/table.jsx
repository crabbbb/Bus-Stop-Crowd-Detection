import { RedirectBtn } from "./redirect_btn";
import { dynamicRoutes } from "../../routes/routes";

export function Table({colName, dataName, rowData, where}) {
    return (
        <div className="mt-5">
            <div className="d-flex flex-row-reverse">
                <p className="cus-font pe-3">Total Record Found :  {rowData.length}</p>
            </div>
            <div class="tableFixHead rounded">
                <table class="table text-center table-hover ">
                    <thead>
                        <tr>
                            {colName.map((col) => (
                                <th scope="col" key={col} className="pt-2 pb-2" style={{"position": "sticky", "top": 0}}>{col}</th>
                            ))}
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        {rowData.map((data) => (
                        <tr key={data[dataName[0]]}>
                            {dataName.map((name) => {
                                if (name === "IsActive") {
                                    return (<td key={`${data[dataName[0]]}-${name}`}>{data["IsActive"] === 0 ? "✅" : "❌"}</td>)
                                } else {
                                    return (<td key={`${data[dataName[0]]}-${name}`}>{data[name]}</td>)
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
            </div>
        </div>
    );
}
