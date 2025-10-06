```java
// 包名
package com.conferencemanagement.model;

import static org.mockito.Mockito.*;
import static org.assertj.core.api.Assertions.*;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

public class UserTest {
    @InjectMocks
    private User user;

    @Mock
    private Calendar calendar;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
        user = new User("1", "John Doe", "john.doe@example.com", "1234567890");
    }

    @Test
    public void should_return_correct_name_when_get_name_called() {
        // Given
        String expectedName = "John Doe";

        // When
        String actualName = user.getName();

        // Then
        assertThat(actualName).isEqualTo(expectedName);
    }

    @Test
    public void should_return_correct_email_when_get_email_called() {
        // Given
        String expectedEmail = "john.doe@example.com";

        // When
        String actualEmail = user.getEmail();

        // Then
        assertThat(actualEmail).isEqualTo(expectedEmail);
    }

    @Test
    public void should_return_correct_phone_when_get_phone_called() {
        // Given
        String expectedPhone = "1234567890";

        // When
        String actualPhone = user.getPhone();

        // Then
        assertThat(actualPhone).isEqualTo(expectedPhone);
    }

    @Test
    public void should_view_calendar_when_viewCalendar_called() {
        // Given
        doNothing().when(calendar).view();

        // When
        user.viewCalendar();

        // Then
        verify(calendar, times(1)).view();
    }
}

public class DefaultWorkspaceTest {
    @InjectMocks
    private DefaultWorkspace defaultWorkspace;

    @Mock
    private Bot bot;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
        defaultWorkspace = new DefaultWorkspace("1", "默认工作区");
    }

    @Test
    public void should_create_default_workspace_when_createDefaultWorkspace_called() {
        // Given

        // When
        defaultWorkspace.createDefaultWorkspace();

        // Then
        verify(defaultWorkspace, times(1)).createDefaultWorkspace();
    }

    @Test
    public void should_invite_member_when_inviteMember_called() {
        // Given
        Member member = new Member("2", new User("3", "Jane Doe", "jane.doe@example.com", "0987654321"));

        // When
        defaultWorkspace.inviteMember(member);

        // Then
        verify(defaultWorkspace, times(1)).inviteMember(member);
    }
}

public class WorkspaceTest {
    @InjectMocks
    private Workspace workspace;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
        workspace = new Workspace("1", "测试工作区");
    }

    @Test
    public void should_add_member_when_addMember_called() {
        // Given
        User user = new User("2", "Jane Doe", "jane.doe@example.com", "0987654321");

        // When
        workspace.addMember(user, "admin");

        // Then
        verify(workspace, times(1)).addMember(user, "admin");
    }

    @Test
    public void should_delete_member_when_deleteMember_called() {
        // Given

        // When
        workspace.deleteMember("2");

        // Then
        verify(workspace, times(1)).deleteMember("2");
    }
}

public class MemberTest {
    @InjectMocks
    private Member member;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
        member = new Member("1", new User("2", "Jane Doe", "jane.doe@example.com", "0987654321"));
    }

    @Test
    public void should_assign_permission_when_assignPermission_called() {
        // Given

        // When
        member.assignPermission("edit");

        // Then
        verify(member, times(1)).assignPermission("edit");
    }

    @Test
    public void should_access_resource_when_accessResource_called() {
        // Given

        // When
        boolean result = member.accessResource("resourceId");

        // Then
        assertThat(result).isTrue();
        verify(member, times(1)).accessResource("resourceId");
    }
}

public class MeetingAssistantTest {
    @InjectMocks
    private MeetingAssistant meetingAssistant;

    @Mock
    private Bot bot;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
        meetingAssistant = new MeetingAssistant("1", "1");
    }

    @Test
    public void should_handle_voice_command_when_onVoiceCommand_called() {
        // Given

        // When
        meetingAssistant.onVoiceCommand("test");

        // Then
        verify(meetingAssistant, times(1)).onVoiceCommand("test");
    }

    @Test
    public void should_translate_text_when_translate_called() {
        // Given
        String sourceLanguage = "en";
        String targetLanguage = "ja";
        String text = "Hello";

        // When
        String result = meetingAssistant.translate(sourceLanguage, targetLanguage, text);

        // Then
        assertThat(result).isEqualTo(bot.translate(sourceLanguage, targetLanguage, text));
        verify(bot, times(1)).translate(sourceLanguage, targetLanguage, text);
    }

    @Test
    public void should_save_recording_when_saveRecording_called() {
        // Given
        String filePath = "file_path";

        // When
        boolean result = meetingAssistant.saveRecording(filePath);

        // Then
        assertThat(result).isEqualTo(bot.saveRecording(filePath));
        verify(bot, times(1)).saveRecording(filePath);
    }
}

public class CalendarTest {
    @InjectMocks
    private Calendar calendar;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
        calendar = new Calendar();
    }

    @Test
    public void should_add_event_when_addEvent_called() {
        // Given
        Event event = new Event();

        // When
        calendar.addEvent(event);

        // Then
        verify(calendar, times(1)).addEvent(event);
    }

    @Test
    public void should_get_events_when_getEvents_called() {
        // Given

        // When
        List<Event> events = calendar.getEvents();

        // Then
        assertThat(events).isEmpty();
        verify(calendar, times(1)).getEvents();
    }

    @Test
    public void should_delete_event_when_deleteEvent_called() {
        // Given

        // When
        calendar.deleteEvent("event_id");

        // Then
        verify(calendar, times(1)).deleteEvent("event_id");
    }
}

public class MeetingRoomTest {
    @InjectMocks
    private MeetingRoom meetingRoom;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
        meetingRoom = new MeetingRoom("1", "测试会议室");
    }

    @Test
    public void should_add_participant_when_addParticipant_called() {
        // Given
        User user = new User("2", "Jane Doe", "jane.doe@example.com", "0987654321");

        // When
        meetingRoom.addParticipant(user, "admin");

        // Then
        verify(meetingRoom, times(1)).addParticipant(user, "admin");
    }

    @Test
    public void should_delete_participant_when_deleteParticipant_called() {
        // Given

        // When
        meetingRoom.deleteParticipant("2");

        // Then
        verify(meetingRoom, times(1)).deleteParticipant("2");
    }

    @Test
    public void should_start_recording_when_startRecording_called() {
        // Given

        // When
        boolean result = meetingRoom.startRecording();

        // Then
        assertThat(result).isTrue();
        verify(meetingRoom, times(1)).startRecording();
    }

    @Test
    public void should_stop_recording_when_stopRecording_called() {
        // Given

        // When
        boolean result = meetingRoom.stopRecording();

        // Then
        assertThat(result).isTrue();
        verify(meetingRoom, times(1)).stopRecording();
    }
}

public class MeetingLogTest {
    @InjectMocks
    private MeetingLog meetingLog;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
        meetingLog = new MeetingLog("user_id", "meeting_id");
    }

    @Test
    public void should_create_log_when_createLog_called() {
        // Given
        String message = "test";
        User fromUser = new User("1", "John Doe", "john.doe@example.com", "1234567890");

        // When
        meetingLog.createLog(message, fromUser);

        // Then
        verify(meetingLog, times(1)).createLog(message, fromUser);
    }

    @Test
    public void should_show_logs_when_showLogs_called() {
        // Given

        // When
        List<MeetingLog> logs = meetingLog.showLogs();

        // Then
        assertThat(logs).isEmpty();
        verify(meetingLog, times(1)).showLogs();
    }

    @Test
    public void should_delete_log_when_deleteLog_called() {
        // Given

        // When
        meetingLog.deleteLog("log_id");

        // Then
        verify(meetingLog, times(1)).deleteLog("log_id");
    }
}

public class WorkSpaceAccessControlTest {
    @InjectMocks
    private WorkSpaceAccessControl workSpaceAccessControl;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
        workSpaceAccessControl = new WorkSpaceAccessControl();
    }

    @Test
    public void should_check_access_when_canAccess_called() {
        // Given

        // When
        boolean result = workSpaceAccessControl.canAccess("resourceId");

        // Then
        assertThat(result).isTrue();
        verify(workSpaceAccessControl, times(1)).canAccess("resourceId");
    }
}

public class DefaultUserRootTest {
    @InjectMocks
    private DefaultUserRoot defaultUserRoot;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
        defaultUserRoot = new DefaultUserRoot(new User("1", "John Doe", "john.doe@example.com", "1234567890"));
    }

    @Test
    public void should_create_default_workspace_when_createDefaultWorkspace_called() {
        // Given

        // When
        defaultUserRoot.createDefaultWorkspace();

        // Then
        verify(defaultUserRoot, times(1)).createDefaultWorkspace();
    }
}

public class DefaultMeetingRoomRootTest {
    @InjectMocks
    private DefaultMeetingRoomRoot defaultMeetingRoomRoot;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
        defaultMeetingRoomRoot = new DefaultMeetingRoomRoot(new MeetingRoom("1", "测试会议室"));
    }

    @Test
    public void should_start_recording_when_startRecording_called() {
        // Given

        // When
        boolean result = defaultMeetingRoomRoot.startRecording();

        // Then
        assertThat(result).isTrue();
        verify(defaultMeetingRoomRoot, times(1)).startRecording();
    }

    @Test
    public void should_stop_recording_when_stopRecording_called() {
        // Given

        // When
        boolean result = defaultMeetingRoomRoot.stopRecording();

        // Then
        assertThat(result).isTrue();
        verify(defaultMeetingRoomRoot, times(1)).stopRecording();
    }
}
```

This solution provides unit test cases for each class in the given code snippet using JUnit and Mockito. Each test case uses Mock objects to mock dependencies and verifies that the methods under test behave as expected. The tests cover various operations such as creating and managing resources, handling user interactions, and managing permissions.