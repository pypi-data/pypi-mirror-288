import { BehaviorSubject } from "rxjs";
import { Component } from "@angular/core";
import {
    BalloonMsgLevel,
    BalloonMsgService,
    BalloonMsgType,
} from "@synerty/peek-plugin-base-js";
import {
    NgLifeCycleEvents,
    TupleActionABC,
    TupleActionPushService,
    TupleDataObserverService,
    TupleSelector,
} from "@synerty/vortexjs";
import { DeviceInfoTable } from "../tuples";
import { UpdateEnrollmentAction } from "@peek/peek_core_device/_private";
import { takeUntil } from "rxjs/operators";
import { DatePipe } from "@angular/common";
import { UpdateOfflineCacheSettingAction } from "../tuples/UpdateOfflineCacheSettingAction";

@Component({
    selector: "core-device-device-info",
    templateUrl: "./device-info.component.html",
    providers: [DatePipe],
})
export class DeviceInfoComponent extends NgLifeCycleEvents {
    private items: DeviceInfoTable[] = [];
    readonly items$ = new BehaviorSubject<DeviceInfoTable[]>([]);

    readonly deviceToken$ = new BehaviorSubject<string | null>(null);
    isOfflineCacheModalShown: boolean = false;

    private _deviceSearchValue: string = "";
    deviceSearchVisible: boolean = false;

    private _userSearchValue: string = "";
    userSearchVisible: boolean = false;

    constructor(
        private balloonMsg: BalloonMsgService,
        private actionService: TupleActionPushService,
        private tupleDataObserver: TupleDataObserverService,
        private datePipe: DatePipe
    ) {
        super();

        // Setup a subscription for the device info data
        tupleDataObserver
            .subscribeToTupleSelector(
                new TupleSelector(DeviceInfoTable.tupleName, {})
            )
            .pipe(takeUntil(this.onDestroyEvent))
            .subscribe((tuples: DeviceInfoTable[]) => {
                this.items = tuples;
                this.refilter();
            });
    }

    get deviceSearchValue(): string {
        return this._deviceSearchValue;
    }

    set deviceSearchValue(value: string) {
        this._deviceSearchValue = (value || "").toLocaleLowerCase();
        this.refilter();
    }

    get userSearchValue(): string {
        return this._userSearchValue;
    }

    set userSearchValue(value: string) {
        this._userSearchValue = (value || "").toLocaleLowerCase();
        this.refilter();
    }

    private refilter(): void {
        const filter = (item: DeviceInfoTable) => {
            if (this.deviceSearchValue.length !== 0) {
                const val = (item.description || "").toLocaleLowerCase();
                if (val.indexOf(this.deviceSearchValue) === -1) return false;
            }
            if (this.userSearchValue.length !== 0) {
                const val = (item.loggedInUser || "").toLocaleLowerCase();
                if (val.indexOf(this.userSearchValue) === -1) return false;
            }
            return true;
        };
        const items = this.items.filter(filter);
        this.items$.next(items);
    }

    deviceStatus(device: DeviceInfoTable): string {
        if (
            device.deviceStatus & DeviceInfoTable.DEVICE_ONLINE &&
            !(device.deviceStatus & DeviceInfoTable.DEVICE_BACKGROUND)
        ) {
            return "Online, App Visible";
        }
        if (
            device.deviceStatus & DeviceInfoTable.DEVICE_ONLINE &&
            device.deviceStatus & DeviceInfoTable.DEVICE_BACKGROUND
        ) {
            return "Online, App Backgrounded";
        }
        if (device.lastOnline) {
            return this.datePipe.transform(device.lastOnline, "medium");
        }
        return "Never Connected";
    }

    deleteDeviceClicked(item) {
        let action = new UpdateEnrollmentAction();
        action.deviceInfoId = item.id;
        action.remove = true;

        this.balloonMsg
            .showMessage(
                "Are you sure you'd like to delete this device?",
                BalloonMsgLevel.Warning,
                BalloonMsgType.ConfirmCancel,
                { confirmText: "Yes", cancelText: "No" }
            )
            .then(() => this.sendAction(action));
    }

    toggleEnrollClicked(item) {
        let action = new UpdateEnrollmentAction();
        action.deviceInfoId = item.id;
        action.unenroll = item.isEnrolled;

        if (!action.unenroll) {
            this.sendAction(action);
            return;
        }

        this.balloonMsg
            .showMessage(
                "Are you sure you'd like to unenroll this device?",
                BalloonMsgLevel.Warning,
                BalloonMsgType.ConfirmCancel,
                { confirmText: "Yes", cancelText: "No" }
            )
            .then(() => this.sendAction(action));
    }

    toggleOfflineCacheEnabledClicked(item: DeviceInfoTable) {
        item.isOfflineCacheEnabled = !item.isOfflineCacheEnabled;
        const action = new UpdateOfflineCacheSettingAction();
        action.deviceInfoId = item.id;
        action.offlineCacheEnabled = item.isOfflineCacheEnabled;

        this.sendAction(action);
    }

    handleShowOfflineCacheStatus(item: DeviceInfoTable) {
        this.deviceToken$.next(item.deviceToken);
        this.isOfflineCacheModalShown = true;
    }

    private sendAction(action: TupleActionABC) {
        this.actionService
            .pushAction(action)
            .then(() => this.balloonMsg.showSuccess("Success"))
            .catch((e) => this.balloonMsg.showError(e));
    }
}
