package test

import (
	"context"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
	"testing"
	"time"

	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/joho/godotenv"
	"github.com/openai/openai-go/v2"
	"github.com/openai/openai-go/v2/option"
	"github.com/stretchr/testify/require"
)

const (
	maxRetries    = 60
	sleepDuration = 30 * time.Second
)

// testModel is a helper function to test the deployed model
func testModel(t *testing.T, publicIP, modelName string) {
	t.Helper()

	if err := godotenv.Load(".env.secure"); err != nil {
		t.Fatalf("failed to load .env.secure: %v", err)
	}

	client := openai.NewClient(
		option.WithAPIKey(os.Getenv("OPENAI_API_KEY")),
		option.WithBaseURL(fmt.Sprintf("http://%s:8000/v1", publicIP)),
	)

	// Wait for the model to be ready
	require.Eventually(t, func() bool {
		_, err := client.Models.List(context.Background())
		return err == nil
	}, maxRetries*sleepDuration, sleepDuration, "model was not ready in time")

	// Send a request to the model
	resp, err := client.Chat.Completions.New(
		context.Background(),
		openai.ChatCompletionNewParams{
			Model: modelName,
			Messages: []openai.ChatCompletionMessageParamUnion{
				openai.UserMessage("Hello there!"),
			},
		},
	)
	t.Log("response: ", resp.Choices[0].Message.Content)
	require.NoError(t, err, "failed to create chat completion")
	require.NotEmpty(t, resp, "got an empty response")
	require.NotEmpty(t, resp.Choices[0].Message.Content, "got an empty message")
}

// TestQwen3_0_6B tests the qwen3-0.6b example
func TestQwen3_0_6B(t *testing.T) {
	t.Parallel()

	terraformOptions := &terraform.Options{
		TerraformDir: "../examples/qwen3-0.6b",
		Vars: map[string]any{
			"allowed_ip_addresses": getMyPublicIP(t),
			"hugging_face_token":   os.Getenv("HUGGING_FACE_TOKEN"),
		},
	}

	// Destroy the previous instance if it exists
	terraform.Destroy(t, terraformOptions)

	defer terraform.Destroy(t, terraformOptions)
	terraform.InitAndApply(t, terraformOptions)

	publicIP := terraform.Output(t, terraformOptions, "public_ip")
	require.NotEmpty(t, publicIP, "public_ip output was empty")

	testModel(t, publicIP, "Qwen/Qwen3-0.6B")
}

// getMyPublicIP returns the public IP of the machine running the test
func getMyPublicIP(t *testing.T) []string {
	t.Helper()

	resp, err := http.Get("https://api.ipify.org")
	require.NoError(t, err, "failed to get public IP")
	defer resp.Body.Close()

	ip, err := io.ReadAll(resp.Body)
	require.NoError(t, err, "failed to read public IP response")

	return []string{fmt.Sprintf("%s/32", strings.TrimSpace(string(ip)))}
}
